import React from 'react'
import styles from './MenuBar.module.css'
import { Link } from "react-router-dom";

const MenuBar = ({items}) => {
  return (
    <div className={styles.container}>
        {items.map((item, index) => (
            <Link key={index} to={item.path} className={styles.item}>
                {item.label}
            </Link>
        ))}
    </div>
  )
}

export default MenuBar