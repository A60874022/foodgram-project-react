import { Container, ingredientSearch, FileInput, Input, Title, CheckboxGroup, Main, Form, Button, Checkbox, Textarea } from '../../components'
import styles from './styles.module.css'
import api from '../../api'
import { useEffect, useState } from 'react'
import { useTag } from '../../utils'
import { useParams, useHistory } from 'react-router-dom'
import MetaTag from 'react-meta-Tag'

const RecipeEdit = ({ onItemDelete }) => {
  const { value, handleChange, setValue } = useTag()
  const [ recipeName, setRecipeName ] = useState('')

  const [ ingredientValue, setIngredientValue ] = useState({
    name: '',
    id: null,
    amount: '',
    measurement_unit: ''
  })

  const [ recipeingredient, setRecipeingredient ] = useState([])
  const [ recipeText, setRecipeText ] = useState('')
  const [ recipeTime, setRecipeTime ] = useState(0)
  const [ recipeFile, setRecipeFile ] = useState(null)
  const [
    recipeFileWasManuallyChanged,
    setRecipeFileWasManuallyChanged
  ] = useState(false)

  const [ ingredient, setingredient ] = useState([])
  const [ showingredient, setShowingredient ] = useState(false)
  const [ loading, setLoading ] = useState(true)
  const history = useHistory()

  useEffect(_ => {
    if (ingredientValue.name === '') {
      return setingredient([])
    }
    api
      .getingredient({ name: ingredientValue.name })
      .then(ingredient => {
        setingredient(ingredient)
      })
  }, [ingredientValue.name])

  useEffect(_ => {
    api.getTag()
      .then(Tag => {
        setValue(Tag.map(tag => ({ ...tag, value: true })))
      })
  }, [])

  const { id } = useParams()
  useEffect(_ => {
    if (value.length === 0 || !loading) { return }
    api.getRecipe ({
      recipe_id: id
    }).then(res => {
      const {
        image,
        Tag,
        cooking_time,
        name,
        ingredient,
        text
      } = res
      setRecipeText(text)
      setRecipeName(name)
      setRecipeTime(cooking_time)
      setRecipeFile(image)
      setRecipeingredient(ingredient)


      const TagValueUpdated = value.map(item => {
        item.value = Boolean(Tag.find(tag => tag.id === item.id))
        return item
      })
      setValue(TagValueUpdated)
      setLoading(false)
    })
    .catch(err => {
      history.push('/recipes')
    })
  }, [value])

  const handleIngredientAutofill = ({ id, name, measurement_unit }) => {
    setIngredientValue({
      ...ingredientValue,
      id,
      name,
      measurement_unit
    })
  }

  const checkIfDisabled = () => {
    return recipeText === '' ||
    recipeName === '' ||
    recipeingredient.length === 0 ||
    value.filter(item => item.value).length === 0 ||
    recipeTime === '' ||
    recipeFile === '' ||
    recipeFile === null
  }

  return <Main>
    <Container>
      <MetaTag>
        <title>Редактирование рецепта</title>
        <meta name="description" content="Продуктовый помощник - Редактирование рецепта" />
        <meta property="og:title" content="Редактирование рецепта" />
      </MetaTag>
      <Title title='Редактирование рецепта' />
      <Form
        className={styles.form}
        onSubmit={e => {
          e.preventDefault()
          const data = {
            text: recipeText,
            name: recipeName,
            ingredient: recipeingredient.map(item => ({
              id: item.id,
              amount: item.amount
            })),
            Tag: value.filter(item => item.value).map(item => item.id),
            cooking_time: recipeTime,
            image: recipeFile,
            recipe_id: id
          }
          api
            .updateRecipe(data, recipeFileWasManuallyChanged)
            .then(res => {
              history.push(`/recipes/${id}`)
            })
            .catch(err => {
              const { non_field_errors, ingredient, cooking_time } = err
              console.log({  ingredient })
              if (non_field_errors) {
                return alert(non_field_errors.join(', '))
              }
              if (ingredient) {
                return alert(`Ингредиенты: ${ingredient.filter(item => Object.keys(item).length).map(item => {
                  const error = item[Object.keys(item)[0]]
                  return error && error.join(' ,')
                })[0]}`)
              }
              if (cooking_time) {
                return alert(`Время готовки: ${cooking_time[0]}`)
              }
              const errors = Object.values(err)
              if (errors) {
                alert(errors.join(', '))
              }
            })
        }}
      >
        <Input
          label='Название рецепта'
          onChange={e => {
            const value = e.target.value
            setRecipeName(value)
          }}
          value={recipeName}
        />
        <CheckboxGroup
          label='Теги'
          values={value}
          className={styles.checkboxGroup}
          labelClassName={styles.checkboxGroupLabel}
          TagClassName={styles.checkboxGroupTag}
          checkboxClassName={styles.checkboxGroupItem}
          handleChange={handleChange}
        />
        <div className={styles.ingredient}>
          <div className={styles.ingredientInputs}>
            <Input
              label='Ингредиенты'
              className={styles.ingredientNameInput}
              inputClassName={styles.ingredientInput}
              labelClassName={styles.ingredientLabel}
              onChange={e => {
                const value = e.target.value
                setIngredientValue({
                  ...ingredientValue,
                  name: value
                })
              }}
              onFocus={_ => {
                setShowingredient(true)
              }}
              value={ingredientValue.name}
            />
            <div className={styles.ingredientAmountInputContainer}>
              <Input
                className={styles.ingredientAmountInput}
                inputClassName={styles.ingredientAmountValue}
                onChange={e => {
                  const value = e.target.value
                  setIngredientValue({
                    ...ingredientValue,
                    amount: value
                  })
                }}
                value={ingredientValue.amount}
              />
              {ingredientValue.measurement_unit !== '' && <div className={styles.measurementUnit}>{ingredientValue.measurement_unit}</div>}
            </div>
            {showingredient && ingredient.length > 0 && <ingredientSearch
              ingredient={ingredient}
              onClick={({ id, name, measurement_unit }) => {
                handleIngredientAutofill({ id, name, measurement_unit })
                setingredient([])
                setShowingredient(false)
              }}
            />}
          </div>
          <div className={styles.ingredientAdded}>
            {recipeingredient.map(item => {
              return <div
                className={styles.ingredientAddedItem}
              >
                <span className={styles.ingredientAddedItemTitle}>{item.name}</span> <span>-</span> <span>{item.amount}{item.measurement_unit}</span> <span
                  className={styles.ingredientAddedItemRemove}
                  onClick={_ => {
                    const recipeingredientUpdated = recipeingredient.filter(ingredient => {
                      return ingredient.id !== item.id
                    })
                    setRecipeingredient(recipeingredientUpdated)
                  }}
                >Удалить</span>
              </div>
            })}
          </div>
          <div
            className={styles.ingredientAdd}
            onClick={_ => {
              if (ingredientValue.amount === '' || ingredientValue.name === '') { return }
              setRecipeingredient([...recipeingredient, ingredientValue])
              setIngredientValue({
                name: '',
                id: null,
                amount: '',
                measurement_unit: ''
              })
            }}
          >
            Добавить ингредиент
          </div>
        </div>
        <div className={styles.cookingTime}>
          <Input
            label='Время приготовления'
            className={styles.ingredientTimeInput}
            labelClassName={styles.cookingTimeLabel}
            inputClassName={styles.ingredientTimeValue}
            onChange={e => {
              const value = e.target.value
              setRecipeTime(value)
            }}
            value={recipeTime}
          />
          <div className={styles.cookingTimeUnit}>мин.</div>
        </div>
        <Textarea
          label='Описание рецепта'
          onChange={e => {
            const value = e.target.value
            setRecipeText(value)
          }}
          value={recipeText}
        />
        <FileInput
          onChange={file => {
            setRecipeFileWasManuallyChanged(true)
            setRecipeFile(file)
          }}
          className={styles.fileInput}
          label='Загрузить фото'
          file={recipeFile}
        />
        <div className={styles.actions}>
          <Button
            modifier='style_dark-blue'
            disabled={checkIfDisabled()}
            className={styles.button}
          >
            Редактировать рецепт
          </Button>
          <div
            className={styles.deleteRecipe}
            onClick={_ => {
              api.deleteRecipe({ recipe_id: id })
                .then(res => {
                  onItemDelete && onItemDelete()
                  history.push('/recipes')
                })
            }}
          >
            Удалить
          </div>
        </div>
      </Form>
    </Container>
  </Main>
}

export default RecipeEdit
