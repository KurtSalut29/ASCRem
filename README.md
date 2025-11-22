# ASCReM - Automated Student Class Record Monitoring System

## 🎯 Project Overview

ASCReM (Automated Student Class Record Monitoring) is a comprehensive web application designed to streamline academic management for instructors. Built with Django and featuring a modern, responsive interface, ASCReM provides automated attendance tracking, grade management, and comprehensive reporting capabilities.

## ✨ Key Features

### 🔐 Authentication & User Management
- **Instructor Login**: Secure login using Instructor ID and 4-digit password
- **Registration**: Complete instructor registration with profile information
- **Profile Management**: Update personal information and profile pictures
- **Settings**: Customizable application settings and preferences

### 📚 Class Management
- **CRUD Operations**: Create, read, update, and delete classes
- **Student Management**: Add, edit, and remove students from classes
- **CSV Import**: Bulk import students from CSV files
- **Class Information**: Track subject, section, semester, and school year

### 📅 Attendance Tracking
- **Real-time Recording**: Mark attendance with Present, Absent, Late, or Excused status
- **Date Management**: Automatic date detection and manual date selection
- **Statistics**: Comprehensive attendance statistics and percentages
- **Dropping List**: Automatic identification of students at risk based on attendance

### 📊 Grade Management
- **Score Input**: Enter quiz, assignment, project, and exam scores
- **Grade Calculation**: Automatic grade calculation with customizable percentages
- **Grade Settings**: Configure grading criteria and passing grades
- **Grade Summary**: Comprehensive grade overview with pass/fail status

### 📈 Dashboard & Analytics
- **Statistics Cards**: Overview of classes, students, and pending grades
- **Interactive Charts**: Visual representation of attendance and grade data
- **Recent Activities**: Activity log with timestamps and descriptions
- **Top Performers**: Display of highest-performing students

### 📋 Report Generation
- **Attendance Reports**: Detailed attendance reports with statistics
- **Grade Reports**: Comprehensive grade reports with analysis
- **Class Summary**: Complete class overview combining attendance and grades
- **Export Options**: PDF and Excel export capabilities

### 🔍 Additional Features
- **Activity Logging**: Track all user actions and system events
- **Responsive Design**: Mobile-friendly interface across all devices
- **Modern UI**: Clean, professional interface with consistent styling
- **Data Validation**: Comprehensive form validation and error handling

## 🛠️ Technology Stack

### Backend
- **Django 5.2.5**: Web framework
- **Django REST Framework**: API development
- **MySQL**: Database management
- **Python 3.10+**: Programming language

### Frontend
- **HTML5**: Markup language
- **CSS3**: Styling with modern features
- **Bootstrap 5.3**: UI framework
- **JavaScript (ES6+)**: Interactive functionality
- **Chart.js**: Data visualization

### Additional Tools
- **Pillow**: Image processing
- **PyMySQL**: MySQL database connector
- **CSV**: Data import/export functionality

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10 or higher
- MySQL 5.7 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd ASCREM
```

### Step 2: Create Virtual Environment
```bash
python -m venv myenv
# On Windows
myenv\Scripts\activate
# On macOS/Linux
source myenv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Database Setup
1. Create a MySQL database named `ascrem`
2. Update database settings in `ASCREM/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'ascrem',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 📁 Project Structure

```
ASCREM/
├── ASCREM/                 # Django project settings
│   ├── __init__.py
│   ├── settings.py         # Project configuration
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI configuration
├── myproject/             # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── forms.py           # Django forms
│   ├── urls.py            # App URL routing
│   ├── admin.py           # Admin configuration
│   └── templates/         # HTML templates
│       ├── dashboard.html
│       ├── attendance.html
│       ├── grades_summary.html
│       ├── reports_panel.html
│       └── reports/       # Report templates
├── static/                # Static files
│   └── images/           # Images and assets
├── media/                # User uploaded files
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

## 🎨 User Interface

### Design Philosophy
- **Modern & Clean**: Professional academic interface
- **Responsive**: Works seamlessly on desktop, tablet, and mobile
- **Intuitive**: Easy-to-use navigation and clear visual hierarchy
- **Consistent**: Uniform styling and behavior across all pages

### Color Scheme
- **Primary**: #1e2fa3 (Deep Blue)
- **Secondary**: #0a0f3c (Dark Navy)
- **Accent**: #ffd700 (Gold)
- **Background**: #0d122e (Dark Background)
- **Text**: #ffffff (White)

### Key UI Components
- **Sidebar Navigation**: Persistent navigation with active states
- **Statistics Cards**: Visual data representation
- **Interactive Tables**: Sortable and filterable data tables
- **Modal Dialogs**: Clean popup interfaces for forms
- **Progress Indicators**: Visual feedback for user actions

## 📊 Database Schema

### Core Models
- **User**: Instructor information and authentication
- **Class**: Class/subject information
- **Student**: Student enrollment and personal data
- **Attendance**: Daily attendance records
- **Score**: Individual student scores
- **GradeSummary**: Calculated final grades
- **ActivityLog**: System activity tracking

### Relationships
- User → Classes (One-to-Many)
- Class → Students (One-to-Many)
- Student → Attendance (One-to-Many)
- Student → Scores (One-to-Many)
- Class → GradeSettings (One-to-One)

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=mysql://user:password@localhost:3306/ascrem
```

### Settings Customization
Key settings in `ASCREM/settings.py`:
- `AUTH_USER_MODEL`: Custom user model
- `MEDIA_URL` & `MEDIA_ROOT`: File upload configuration
- `STATIC_URL` & `STATICFILES_DIRS`: Static file serving
- `LOGIN_URL` & `LOGIN_REDIRECT_URL`: Authentication settings

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG = False` in settings
2. Configure production database
3. Set up static file serving
4. Configure media file handling
5. Set up SSL/HTTPS
6. Configure email settings
7. Set up logging
8. Run security checks

### Recommended Hosting
- **VPS**: DigitalOcean, Linode, AWS EC2
- **Platform**: Heroku, PythonAnywhere
- **Database**: AWS RDS, Google Cloud SQL

## 📱 Mobile Responsiveness

The application is fully responsive and optimized for:
- **Desktop**: Full feature set with sidebar navigation
- **Tablet**: Adapted layout with collapsible sidebar
- **Mobile**: Stacked layout with mobile-friendly navigation

## 🔒 Security Features

- **CSRF Protection**: Built-in Django CSRF tokens
- **SQL Injection Prevention**: Django ORM protection
- **XSS Protection**: Template auto-escaping
- **Authentication**: Secure login system
- **File Upload Security**: Validated file types and sizes

## 🧪 Testing

### Running Tests
```bash
python manage.py test
```

### Test Coverage
- Model validation
- View functionality
- Form processing
- Authentication flows
- API endpoints

## 📈 Performance Optimization

### Database Optimization
- Efficient queries with select_related
- Database indexing on frequently queried fields
- Pagination for large datasets

### Frontend Optimization
- Minified CSS and JavaScript
- Optimized images
- Lazy loading for charts
- Efficient DOM manipulation

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Maintain consistent indentation

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔄 Version History

### Version 1.0.0 (Current)
- Initial release
- Complete authentication system
- Class and student management
- Attendance tracking
- Grade management
- Report generation
- Responsive UI

## 🎯 Future Enhancements

### Planned Features
- **Mobile App**: Native mobile application
- **API Integration**: RESTful API for external systems
- **Advanced Analytics**: Machine learning insights
- **Multi-language Support**: Internationalization
- **Cloud Storage**: Integration with cloud services
- **Real-time Notifications**: Push notifications
- **Advanced Reporting**: More report types and formats

## 📞 Contact Information

- **Project Lead**: [Your Name]
- **Email**: [your.email@example.com]
- **GitHub**: [github.com/yourusername]

---

**ASCReM** - Streamlining Academic Management with Technology

*Built with ❤️ using Django and modern web technologies*
