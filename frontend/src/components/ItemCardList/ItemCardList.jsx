import React from 'react'
import styles from './ItemCardList.module.css'

const ItemCardList = ({ items, unit }) => {
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
              <div className={styles.exerciseTimeFont}>{item.calories} {unit}</div>
              <div className={styles.exerciseTimeFont}>{item.time ? `${item.time} min` : ''}</div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

export default ItemCardList