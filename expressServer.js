import express from 'express';
import mysql   from 'mysql';
import bodyParser from 'body-parser';
import cors from 'cors';

const app  = express();
const port = 5000;

// Enable CORS for all routes
app.use(cors());

// Parse JSON in request bodies
app.use(bodyParser.json());

// MySQL connection
const db = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : 'sqlpass123',
  database : 'Stack'
});

db.connect(err => {
  if (err) {
    console.error('Error connecting to MySQL:', err);
    process.exit(1);
  }
  console.log('Connected to MySQL database');
});

/* ─────────────  REGISTER  ───────────── */
app.post('/users', (req, res) => {
  console.log('Incoming request body:', req.body);

  const { firstName, lastName, email, password, confirmPassword } = req.body;

  if (!firstName || !lastName || !email || !password || !confirmPassword) {
    return res.status(400).json({ message: 'All fields are required' });
  }
  if (password !== confirmPassword) {
    return res.status(400).json({ message: 'Passwords do not match' });
  }

  db.query('SELECT * FROM User WHERE Email = ?', [email], (err, rows) => {
    if (err) {
      console.error('Email-check error:', err);
      return res.status(500).json({ message: 'Database error' });
    }
    if (rows.length) {
      return res.status(400).json({ message: 'Email is already registered' });
    }

    const sql = 'INSERT INTO User (Firstname, Lastname, Email, Password) VALUES (?, ?, ?, ?)';
    db.query(sql, [firstName, lastName, email, password], (err, result) => {
      if (err) {
        console.error('Insert error:', err);
        return res.status(500).json({ message: 'Insert error' });
      }
      res.status(201).json({ message: 'User registered successfully', userId: result.insertId });
    });
  });
});

console.log(' EXPRESS FILE LOADED  >>>  ' + __filename);
/* ─────────────  LOGIN  ───────────── */
app.post('/users/login', (req, res) => {
    console.log(' /users/login route HIT  >>>', req.body);
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ message: 'Email and password are required' });
  }

  const sql = 'SELECT * FROM User WHERE Email = ? AND Password = ?';
  db.query(sql, [email, password], (err, rows) => {
    if (err) {
      console.error('Login DB error:', err);
      return res.status(500).json({ message: 'Database error' });
    }
    if (rows.length === 0) {
      return res.status(401).json({ message: 'Invalid email or password' });
    }
    res.json({ message: 'Login successful', userId: rows[0].UserID });
  });
});

/* ─────────────  ROOT  ───────────── */
app.get('/', (_req, res) => res.send('Hello World from Express!'));

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
