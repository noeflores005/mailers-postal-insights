// Make load failures visible instead of leaving a blank or half-filled chart.
window.addEventListener('error', event => {
  if (event.target && event.target.tagName === 'IMG') return;
  const main = document.querySelector('main');
  if (!main) return;
  const section = document.createElement('section');
  section.className = 'card'; section.setAttribute('role','alert');
  const title = document.createElement('h2'); title.textContent = 'The dashboard could not load this view.';
  const text = document.createElement('p'); text.textContent = 'Reload the page. If you opened a downloaded copy, extract the whole project and keep its data and assets folders beside index.html. No data was changed.';
  section.append(title,text);main.replaceChildren(section);
}, true);
