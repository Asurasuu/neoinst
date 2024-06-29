// Функция для установки темы
function setTheme(theme) {
  document.body.className = theme;
  localStorage.setItem('theme', theme);
}

// Загрузка сохраненной темы при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    setTheme(savedTheme);
  }
});

// Обработчик для переключения темы
document.getElementById('themeToggle').addEventListener('click', function() {
  const currentTheme = document.body.className;
  const newTheme = currentTheme === 'light-theme' ? 'dark-theme' : 'light-theme';
  setTheme(newTheme);
});
