import React from 'react'
import styles from './ItemCardListGoals.module.css'

const ItemCardListGoals = ({ items }) => {
  return (
    <div>
      {items.map(item => (
        <div className={styles.containerFlexLeft} key={item.id}>
          <div className={styles.iconBox}>
            <i className={`bx bx-${item.iconClass}`}></i>
          </div>
          <div className={styles.exerciseDescriptionBox}>
            <div className={styles.titleWater}>{item.name}</div>
            <div className={styles.containerFlex}>
              <div className={styles.exerciseTimeFont}>{item.description} {item.unit}</div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default ItemCardListGoals