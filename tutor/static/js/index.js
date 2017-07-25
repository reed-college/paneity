//This code makes the search function on index.html work.
//it filters the list elements by the input you give it and returns the
//elements that match your input
function myFunctionExport() {
  const input = document.getElementById('myInput');
  const filter = input.value.toUpperCase();
  const ul = document.getElementById('myUL');
  const li = ul.getElementsByTagName('li');
  for (let i = 0; i < li.length; i += 1) {
    const a = li[i].getElementsByTagName('a')[0];
    if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = '';
    } else {
      li[i].style.display = 'none';
    }
  }
}
