const fs = require('fs');
const ELK = require('elkjs');
const elk = new ELK();

const input = JSON.parse(fs.readFileSync('elk_input.json', 'utf8'));

elk.layout(input)
  .then(output => {
    fs.writeFileSync('elk_output.json', JSON.stringify(output, null, 2));
    console.log("✅ ELK layout complete → elk_output.json");
  })
  .catch(err => {
    console.error("❌ ELK layout failed:", err);
  });
