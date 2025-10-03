import React from "react";
import { NavLink } from "react-router-dom";
import styles from "./Navbar.module.css";

const Navbar = () => {
  return (
    <nav className={styles.navbar}>
      <NavLink 
        to="/dashboard"
        className={({ isActive }) => `${styles.navButton} ${isActive ? styles.active : ""}`}
      >
        <i className={`bx bx-home ${styles.icon}`}></i>
      </NavLink>
      
      <NavLink 
        to="/food"
        className={({ isActive }) => `${styles.navButton} ${isActive ? styles.active : ""}`}
      >
        <i className={`bx bx-pizza ${styles.icon}`}></i>
      </NavLink>

      <NavLink 
        to="/exercises"
        className={({ isActive }) => `${styles.navButton} ${isActive ? styles.active : ""}`}
      >
        <i className={`bx bx-dumbbell ${styles.icon}`}></i>
      </NavLink>


      <NavLink 
        to="/profile"
        className={({ isActive }) => `${styles.navButton} ${isActive ? styles.active : ""}`}
      >
        <i className={`bx bx-user ${styles.icon}`}></i>
      </NavLink>
    </nav>
  );
};

export default Navbar;