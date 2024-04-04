const ExcelJS = require('exceljs');
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

// Create a new Excel workbook and worksheet
const workbook = new ExcelJS.Workbook();
const worksheet = workbook.addWorksheet('ScannedData');
worksheet.columns = [{ header: 'Name', key: 'name' }];

// Endpoint to receive scanned data
app.post('/', (req, res) => {
  const { name } = req.body;
  
  // Add scanned name to Excel sheet
  worksheet.addRow({ name });

  // Save the workbook
  workbook.xlsx.writeFile('scanned_data.xlsx')
    .then(() => {
      console.log('Scanned data saved to Excel sheet');
      res.sendStatus(200);
    })
    .catch(err => {
      console.error('Error saving scanned data:', err);
      res.status(500).send('Error saving scanned data');
    });
});

// Start the server
const port = 3000;
app.listen(port, () => {
  console.log(`Server is running on http://localhost:3000`);
});