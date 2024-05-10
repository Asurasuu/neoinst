import React from 'react';
import './style.css';
import menu from './menu.png';
import setting  from './setting.png';
import ava from './ava.png';
import telegram from './telegram.png';
import instagram from './instagram.png';
import dribble from './dribble.png';

function Profile() {
  return (
    <div>
      <div className="container">
        <div className="profile-box">
          <img src={menu} className="menu-icon" alt="Menu icon" />
          <img src={setting} className="setting-icon" alt="Setting icon" />
          <img src={ava} className="ava-icon" alt="Avatar" />
          <h3>Kenneth Amedalov</h3>
          <p>General manager Echpochmak</p>
          <div className="icons">
            <a href="https://t.me/Kenneth0fficial">
              <img className="image" src={telegram} alt="Telegram" />
            </a>
            <a href="https://www.instagram.com/ahmetovkanat840?igsh=MzRlODBiNWFlZA==">
              <img className="image" src={instagram} alt="Instagram" />
            </a>
            <a href="https://vk.com/kanat845">
              <img className="image" src={dribble} alt="Dribble" />
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Profile;
