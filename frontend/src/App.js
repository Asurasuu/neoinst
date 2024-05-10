// App.js
import React from 'react';
import { Link } from 'react-router-dom';
import './style/App.css';
import heart from './components/heart.png';
import home from './components/home.png';
import interesting from './components/interesting.png';
import mess from './components/mess.png';
import plus from './components/plus.png';
import search from './components/search.png';
import threeDots from './components/threeDots.png';
import user from './components/user.png';

function App() {
  return (
    <div className="App">
      <div className='oneСolumn'> 
        {/* Тут будет лого */}
        <p align="center"> 
          <img align="left" src={home} width="18%"/> <p align="center">Главная</p>
        </p>

        <p align="center"> 
          <img align="left" src={search} width="18%"/>  <p align="center">Поиск</p>
        </p>

        <p align="center"> 
          <img align="left" src={mess} width="18%"/> <p align="center">Сообщения</p>
        </p>

        <p align="center"> 
          <img align="left" src={interesting} width="18%"/> <p align="center">Интересное</p>
        </p>

        <p align="center"> 
          <img align="left" src={heart} width="18%"/> <p align="center">Уведомления</p>
        </p>



          <p align="center" className='oneColumnBottom'> 
            <img align="left" src={plus} width="18%"/> <p align="center">Добавить</p>
          </p>

          <p align="center"> 
            <img align="left" src={user} width="18%"/> 
            <p align="center">
              <Link to="/profile">Профиль</Link>
            </p>
          </p>

      </div>
      
      <div className='twoСolumn'>
        {/* Лента */}
        Лента
      </div>

      <div className='threeСolumn'>
        {/* Контакты */}
        Контакты
      </div>

    </div>
  );
}

export default App;