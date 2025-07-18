# FastReckon: Best Practice for Personal Financial Management

    FastReckon offers a sophisticated solution for personal financial management by incorporating the corporate practice of double-ledger accounting, all while ensuring a user-friendly experience.

## 🚀 Key Features

- **Easy Bookkeeping Input**: Streamlined forms for quick and easy data entry.
- **Comprehensive Financial Reports**: Generate insightful reports to analyze your financial health.
- **Double-Ledger Accounting**: Stay organized and accountable with a robust accounting method.
- **User-Friendly Interface**: Designed with user experience in mind, making finance management accessible to everyone.

## 🌟 Benefits

- **Stay Organized**: Keep your financial transactions organized in one place.
- **Informed Decision Making**: Utilize in-depth analysis and reports to make smarter financial decisions.
- **Customizable**: Tailor the application to fit your specific financial needs.

## 📦 Installation

To get started with FastReckon, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Thee5176/FastReckon.git
   cd FastReckon
   ```

2. **Set Credential Key for Environment files**

   ```
   DJANGO_SECRET_KEY='7i&$x%%lq3v-cebdutn2^$b@#k76d*e*m*-b%ksgnmns4-@!+5'
   DJANGO_DEBUG='False'

   POSTGRES_USER='fastreckon-admin'
   POSTGRES_PASSWORD='password'
   POSTGRES_DB='fastreckon'

   SENDGRID_PASSWORD=''

   SOCIALACCOUNT_GOOGLE_CLIENT_ID=''
   SOCIALACCOUNT_GOOGLE_SECRET=''

   SOCIALACCOUNT_GITHUB_CLIENT_ID=''
   SOCIALACCOUNT_GITHUB_SECRET=''
   ```

3. **Run SetUp Script**

   ```bash
   docker compose build
   docker compose up -d
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py loaddata _testdata/backup.json
   ```
4. **Visit Landing Page**
localhost:8009

- username: admin
- password: Pass_1234
## 📈 Development

### Set up Phrase

- branch : `setup`

- objective : set up developing environment
  - User management(login/logout/password)
  - Custom user admin interface
  - Create base
  - Static files management using Whitenoise
  - Email notification using SendGrid
  - Beautiful templates using Bootstrap
  - hosting with Gunicorn on Heroku

### MVP Phrase

- branch : `main`

- objective :
  - Implement CRUD operations for transaction management
  - Create a normalized model for transaction data
  - transaction records in a user-friendly table view
  - Import CSV file to the database for easy bulk uploads

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](https://www.mit.edu/~amini/LICENSE.md) file for more details.

## 📫 Contact

For questions, feedback, or support, feel free to reach out:

- Email: <theerapong5176@gmail.com>
