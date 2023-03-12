import styles from './styles.module.css'
import cn from 'classnames'
import { Tag } from '../index'

const TagContainer = ({ Tag }) => {
  if (!Tag) { return null }
  return <div className={styles['Tag-container']}>
    {Tag.map(tag => {
      return <Tag
        key={tag.id}
        color={tag.color}
        name={tag.name}
      />
    })}
  </div>
}

export default TagContainer
