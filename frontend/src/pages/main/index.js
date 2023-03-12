import { Card, Title, Pagination, CardList, Container, Main, CheckboxGroup  } from '../../components'
import styles from './styles.module.css'
import { useRecipes } from '../../utils/index.js'
import { useEffect } from 'react'
import api from '../../api'
import MetaTag from 'react-meta-Tag'

const HomePage = ({ updateOrders }) => {
  const {
    recipes,
    setRecipes,
    recipesCount,
    setRecipesCount,
    recipesPage,
    setRecipesPage,
    TagValue,
    setTagValue,
    handleTagChange,
    handleLike,
    handleAddToCart
  } = useRecipes()


  const getRecipes = ({ page = 1, Tag }) => {
    api
      .getRecipes({ page, Tag })
      .then(res => {
        const { results, count } = res
        setRecipes(results)
        setRecipesCount(count)
      })
  }

  useEffect(_ => {
    getRecipes({ page: recipesPage, Tag: TagValue })
  }, [recipesPage, TagValue])

  useEffect(_ => {
    api.getTag()
      .then(Tag => {
        setTagValue(Tag.map(tag => ({ ...tag, value: true })))
      })
  }, [])


  return <Main>
    <Container>
      <MetaTag>
        <title>Рецепты</title>
        <meta name="description" content="Продуктовый помощник - Рецепты" />
        <meta property="og:title" content="Рецепты" />
      </MetaTag>
      <div className={styles.title}>
        <Title title='Рецепты' />
        <CheckboxGroup
          values={TagValue}
          handleChange={value => {
            setRecipesPage(1)
            handleTagChange(value)
          }}
        />
      </div>
      <CardList>
        {recipes.map(card => <Card
          {...card}
          key={card.id}
          updateOrders={updateOrders}
          handleLike={handleLike}
          handleAddToCart={handleAddToCart}
        />)}
      </CardList>
      <Pagination
        count={recipesCount}
        limit={6}
        page={recipesPage}
        onPageChange={page => setRecipesPage(page)}
      />
    </Container>
  </Main>
}

export default HomePage

