import pytest
from rest_framework.test import APIClient
from courses.models import Course
from users.models import User, Instructor, Student
from rest_framework import status

@pytest.mark.django_db
class TestCourseView:

    def test_get_courses(self):
        instructor = Instructor.objects.create(user=User.objects.create_user(username="instructor1", password="password"))
        Course.objects.create(
            title="Test Course 1",
            description="Test Course Description 1",
            created_by=instructor,
            duration=10,
            difficulty="beginner",
            subject="Math"
        )
        client = APIClient()
        response = client.get('/courses/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) > 0  # Ensure there is at least one course

@pytest.mark.django_db
class TestCourseDetailView:

    def test_get_course_detail(self):
        user = User.objects.create_user(username="student2", password="testpass")
        student = Student.objects.create(user=user)
        instructor = Instructor.objects.create(user=User.objects.create_user(username="instructor1", password="password"))
        course = Course.objects.create(
            title="Test Course 1",
            description="Test Course Description 1",
            created_by=instructor,
            duration=10,
            difficulty="beginner",
            subject="Math"
        )
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(f'/courses/{course.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == course.id
        assert response.data['title'] == course.title
        assert response.data['description'] == course.description
        assert response.data['subject'] == course.subject
        assert response.data['created_by'] == instructor.id


@pytest.mark.django_db
class TestAddCourseView:

    def test_add_course(self):
        admin_user = User.objects.create_superuser(username="admin", password="admin")
        instructor = Instructor.objects.create(user=User.objects.create_user(username="instructor1", password="password"))

        course_data = {
            "title": "New Course",
            "description": "Description of the new course",
            "created_by": instructor.id,
            "duration": 10,
            "difficulty": "beginner",
            "subject": "Math"
        }
        client = APIClient()
        client.force_authenticate(user=admin_user)
        response = client.post('/courses/add/', course_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == "New Course"
        assert response.data['created_by'] == instructor.id


@pytest.mark.django_db
class TestUpdateDeleteCourseView:

    def test_update_course(self):
        admin_user = User.objects.create_superuser(username="admin", password="admin")
        instructor = Instructor.objects.create(user=User.objects.create_user(username="instructor1", password="password"))
        course = Course.objects.create(
            title="Test Course 1",
            description="Test Course Description 1",
            created_by=instructor,
            duration=10,
            difficulty="beginner",
            subject="Math"
        )        
        updated_data = {
            "title": "Updated Course Title",
            "description": "Updated Description",
            "created_by": instructor.id,
            "duration": 15,
            "difficulty": "intermediate",
            "subject": "Science"
        }

        client = APIClient()
        client.force_authenticate(user=admin_user)
        response = client.put(f'/courses/update-delete/{course.id}/', updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == "Updated Course Title"

    def test_delete_course(self):
        admin_user = User.objects.create_superuser(username="admin", password="adminpass")
        instructor = Instructor.objects.create(user=User.objects.create_user(username="instructor1", password="password"))
        course = Course.objects.create(
            title="Test Course 1",
            description="Test Course Description 1",
            created_by=instructor,
            duration=10,
            difficulty="beginner",
            subject="Math"
        )

        client = APIClient()
        client.force_authenticate(user=admin_user)
        response = client.delete(f'/courses/update-delete/{course.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Course.objects.filter(id=course.id).exists()
