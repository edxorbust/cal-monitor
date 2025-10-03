import React from 'react'
import styles from './ItemCardListSettings.module.css'

const ItemCardListSettings = ({ items }) => {
  return (
    <div>
      {items.map(item => (
        <div className={styles.containerFlexLeft} key={item.id}>
          <div className={styles.iconBox}>
            <i className={`bx bx-${item.iconClass}`}></i>
          </div>
          <div className={styles.exerciseDescriptionBox}>
            <div className={styles.titleWater}>{item.name}</div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default ItemCardListSettings