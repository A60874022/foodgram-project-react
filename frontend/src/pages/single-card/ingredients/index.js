import styles from './styles.module.css'

const ingredient = ({ ingredient }) => {
  if (!ingredient) { return null }
  return <div className={styles.ingredient}>
    <h3 className={styles['ingredient__title']}>Ингредиенты:</h3>
    <div className={styles['ingredient__list']}>
      {ingredient.map(({
        name,
        amount,
        measurement_unit
      }) => <p
        key={`${name}${amount}${measurement_unit}`}
        className={styles['ingredient__list-item']}
      >
        {name} - {amount} {measurement_unit}
      </p>)}
    </div>
  </div>
}

export default ingredient

