// Load and display country rankings
fetch('country_scoreboard.json')
  .then(res => res.json())
  .then(data => {
    const tbody = document.querySelector('#country-scoreboard tbody');
    data.forEach((country, idx) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${idx + 1}</td>
        <td>${country.country}</td>
        <td>${country.total}</td>
        <td>${country.num_contestants}</td>
        <td>${country.checked}</td>
      `;
      tbody.appendChild(tr);
    });
  })
  .catch(err => {
    document.querySelector('#country-scoreboard tbody').innerHTML = '<tr><td colspan="4">Failed to load data.</td></tr>';
  });

// Load and display contestant rankings
fetch('scoreboard.json')
  .then(res => res.json())
  .then(data => {
    const tbody = document.querySelector('#scoreboard tbody');
    data.sort((a, b) => b.total - a.total);
    data.forEach((team, idx) => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${idx + 1}</td>
        <td>${team.country}</td>
        <td>${team.P1}</td>
        <td>${team.P2}</td>
        <td>${team.P3}</td>
        <td>${team.P4}</td>
        <td>${team.P5}</td>
        <td>${team.P6}</td>
        <td>${team.total}</td>
        <td>${team.checked}</td>
      `;
      tbody.appendChild(tr);
    });
  })
  .catch(err => {
    document.querySelector('#scoreboard tbody').innerHTML = '<tr><td colspan="9">Failed to load data.</td></tr>';
  }); 