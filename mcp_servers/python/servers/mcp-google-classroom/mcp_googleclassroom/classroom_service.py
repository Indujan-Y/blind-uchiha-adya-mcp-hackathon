from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import json
import os
from typing import Optional, Dict, Any, List, Union
from datetime import datetime, time
import logging

logger = logging.getLogger(__name__)

SCOPES = [
    'https://www.googleapis.com/auth/classroom.courses',
    'https://www.googleapis.com/auth/classroom.rosters',
    'https://www.googleapis.com/auth/classroom.coursework.students',
    'https://www.googleapis.com/auth/classroom.coursework.me',
    'https://www.googleapis.com/auth/classroom.profile.emails',
    'https://www.googleapis.com/auth/classroom.profile.photos',
    'https://www.googleapis.com/auth/classroom.announcements',
]

class ClassroomServiceError(Exception):
    """Custom exception for Classroom service errors."""
    pass

class ClassroomService:
    def __init__(self, credentials: Dict[str, Any] = None, token_path: str = 'token.json'):
        """
        Initialize the Classroom service with OAuth2 credentials.

        Args:
            credentials (dict): OAuth2 client credentials dictionary
            token_path (str): Path to store/retrieve OAuth2 token
        """
        self.credentials = credentials
        self.token_path = token_path
        self.service = self._build_service()

    def _display_token_info(self, creds):
        """Display OAuth2 token information and save to token_info.json"""
        print("\n" + "="*60)
        print("OAUTH2 TOKEN INFORMATION")
        print("="*60)
        print(f"Access Token: {creds.token}")
        print(f"Refresh Token: {creds.refresh_token}")
        print(f"Client ID: {creds.client_id}")
        print(f"Client Secret: {creds.client_secret}")
        print(f"Token URI: {creds.token_uri}")
        print(f"Scopes: {', '.join(creds.scopes) if creds.scopes else 'None'}")
        if creds.expiry:
            print(f"Token Expires: {creds.expiry}")
        else:
            print("Token Expires: Not set")
        print("="*60)
        token_info = {
            "access_token": creds.token,
            "refresh_token": creds.refresh_token,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "token_uri": creds.token_uri,
            "scopes": creds.scopes,
            "expiry": creds.expiry.isoformat() if creds.expiry else None
        }
        with open('token_info.json', 'w') as f:
            json.dump(token_info, f, indent=2)
        logger.info("Token information saved to token_info.json")

    def _build_service(self):
        """Build the Google Classroom service object using OAuth2, with robust token management."""
        creds = None
        # Load existing token if available
        if os.path.exists(self.token_path):
            try:
                creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
                logger.info("Loaded existing credentials from token file")
            except Exception as e:
                logger.warning(f"Failed to load existing token: {str(e)}")
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    logger.info("Refreshed expired credentials")
                except Exception as e:
                    logger.error(f"Failed to refresh credentials: {e}")
                    creds = None
            if not creds:
                if not self.credentials:
                    raise ClassroomServiceError("Credentials dictionary is required")
                
                # Create a temporary credentials file for OAuth2 flow
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                    json.dump(self.credentials, temp_file)
                    temp_credentials_path = temp_file.name
                
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        temp_credentials_path, SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                    logger.info("Completed OAuth2 flow")
                    self._display_token_info(creds)
                finally:
                    # Clean up temporary file
                    os.unlink(temp_credentials_path)
            
            # Save the credentials for the next run
            try:
                with open(self.token_path, 'w') as token:
                    token.write(creds.to_json())
                logger.info(f"Saved credentials to {self.token_path}")
            except Exception as e:
                logger.warning(f"Failed to save token: {str(e)}")
        return build('classroom', 'v1', credentials=creds)

    def get_fresh_tokens(self):
        """Force OAuth2 flow to get fresh tokens and display info."""
        if not self.credentials:
            raise ClassroomServiceError("Credentials dictionary is required")
        if os.path.exists(self.token_path):
            os.remove(self.token_path)
            logger.info("Removed existing token file")
        
        # Create a temporary credentials file for OAuth2 flow
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
            json.dump(self.credentials, temp_file)
            temp_credentials_path = temp_file.name
        
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                temp_credentials_path, SCOPES
            )
            creds = flow.run_local_server(port=0)
            logger.info("Completed fresh OAuth2 authentication")
            self._display_token_info(creds)
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())
            logger.info(f"Saved fresh credentials to {self.token_path}")
            self.service = build('classroom', 'v1', credentials=creds)
            return creds
        finally:
            # Clean up temporary file
            os.unlink(temp_credentials_path)

    def show_current_token_info(self):
        """Display current token information if available."""
        if not os.path.exists(self.token_path):
            print("No token file found. Please authenticate first.")
            return
        try:
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
            self._display_token_info(creds)
        except Exception as e:
            print(f"Error reading token file: {e}")

    def _paginate_results(self, request_func, **kwargs) -> List[Dict[str, Any]]:
        """Helper method to handle pagination for list operations."""
        results = []
        next_page_token = None
        
        while True:
            if next_page_token:
                kwargs['pageToken'] = next_page_token
            
            response = request_func(**kwargs).execute()
            
            # Get the appropriate key for results (courses, students, etc.)
            for key in ['courses', 'students', 'teachers', 'courseWork', 'studentSubmissions', 'announcements']:
                if key in response:
                    results.extend(response[key])
                    break
            
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        
        return results
    
    def _handle_api_error(self, operation: str, error: Exception) -> None:
        """Centralized error handling for API operations."""
        error_msg = f"Failed to {operation}: {str(error)}"
        logger.error(error_msg)
        raise ClassroomServiceError(error_msg)

    def create_course(self, name: str, section: Optional[str] = None, description: Optional[str] = None,
                      description_heading: Optional[str] = None, room: Optional[str] = None,
                      owner_id: str = "me", course_state: str = "ACTIVE") -> Dict[str, Any]:
        """
        Create a new Google Classroom course.

        Args:
            name (str): Name of the course (required)
            section (str, optional): Section name
            description (str, optional): Course description
            description_heading (str, optional): Description heading
            room (str, optional): Room location
            owner_id (str): Owner identifier (default "me")
            course_state (str): Course state (default "ACTIVE")

        Returns:
            dict: Created course details
        """
        try:
            course_body = {
                'name': name,
                'ownerId': owner_id,
                'courseState': course_state
            }
            if section:
                course_body['section'] = section
            if description:
                course_body['description'] = description
            if description_heading:
                course_body['descriptionHeading'] = description_heading
            if room:
                course_body['room'] = room

            result = self.service.courses().create(body=course_body).execute()
            logger.info(f"Successfully created course: {result.get('name')} (ID: {result.get('id')})")
            return result
        except Exception as e:
            self._handle_api_error("create course", e)

    def list_courses(
        self,
        teacher_id: Optional[str] = None,
        student_id: Optional[str] = None,
        course_states: Optional[List[str]] = None,
        page_size: int = 100,
        paginate_all: bool = False
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        List courses in Google Classroom.

        Args:
            teacher_id (str, optional): Filter by teacher ID.
            student_id (str, optional): Filter by student ID.
            course_states (list, optional): Filter by course states.
            page_size (int): Number of courses to return per page.
            paginate_all (bool): If True, return all results across all pages.

        Returns:
            dict or list: Courses data (raw API response or list of all courses).
        """
        print(f"teacher_id: {teacher_id}"  )
        print(f"student_id: {student_id}"  )
        print(f"course_states: {course_states}"  )
        print(f"page_size: {page_size}"  )
        print(f"paginate_all: {paginate_all}"  )
        try:
            request_params = {'pageSize': page_size}

            if teacher_id:
                request_params['teacherId'] = teacher_id
            if student_id:
                request_params['studentId'] = student_id
            if course_states:
                request_params['courseStates'] = course_states

            if paginate_all:
                return self._paginate_results(self.service.courses().list, **request_params)
            else:
                return self.service.courses().list(**request_params).execute()

        except Exception as e:
            self._handle_api_error("list courses", e)

    def get_course(self, course_id: str) -> Dict[str, Any]:
        """
        Get details of a specific course.

        Args:
            course_id (str): Course ID.

        Returns:
            dict: Course details.
        """
        try:
            if not course_id:
                raise ClassroomServiceError("Course ID is required")
            return self.service.courses().get(id=course_id).execute()
        except Exception as e:
            self._handle_api_error(f"get course {course_id}", e)
        
    def update_course(self, course_id: str, name: Optional[str] = None, section: Optional[str] = None,
                     description: Optional[str] = None, description_heading: Optional[str] = None,
                     room: Optional[str] = None, course_state: Optional[str] = None,
                     owner_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Update an existing course (PATCH).

        Args:
            course_id (str): Course ID.
            name (str, optional): New name
            section (str, optional): New section
            description (str, optional): New description
            description_heading (str, optional): New description heading
            room (str, optional): New room
            course_state (str, optional): New course state
            owner_id (str, optional): New owner

        Returns:
            dict: Updated course details.
        """
        try:
            if not course_id:
                raise ClassroomServiceError("Course ID is required")

            update_body = {}
            update_mask = []

            if name is not None:
                update_body['name'] = name
                update_mask.append('name')
            if section is not None:
                update_body['section'] = section
                update_mask.append('section')
            if description is not None:
                update_body['description'] = description
                update_mask.append('description')
            if description_heading is not None:
                update_body['descriptionHeading'] = description_heading
                update_mask.append('descriptionHeading')
            if room is not None:
                update_body['room'] = room
                update_mask.append('room')
            if course_state is not None:
                update_body['courseState'] = course_state
                update_mask.append('courseState')
            if owner_id is not None:
                update_body['ownerId'] = owner_id
                update_mask.append('ownerId')

            if not update_mask:
                raise ClassroomServiceError("No valid fields to update")

            result = self.service.courses().patch(
                id=course_id,
                body=update_body,
                updateMask=','.join(update_mask)
            ).execute()
            logger.info(f"Successfully updated course {course_id}")
            return result
        except Exception as e:
            self._handle_api_error(f"update course {course_id}", e)

    def delete_course(self, course_id: str) -> Dict[str, Any]:
        """
        Archive a course (Google Classroom does not support actual deletion).

        Args:
            course_id (str): Course ID.

        Returns:
            dict: Archived course details.
        """
        try:
            if not course_id:
                raise ClassroomServiceError("Course ID is required")

            course_data = {'courseState': 'ARCHIVED'}
            result = self.service.courses().patch(
                id=course_id,
                body=course_data,
                updateMask='courseState'
            ).execute()
            logger.info(f"Successfully archived course {course_id}")
            return result
        except Exception as e:
            self._handle_api_error(f"archive course {course_id}", e)

    def get_course_summary(self, course_id: str) -> Dict[str, Any]:
        """
        Get a comprehensive summary of a course including students, teachers, and assignments.
        
        Args:
            course_id (str): Course ID
            
        Returns:
            dict: Course summary with all related data
        """
        try:
            course = self.get_course(course_id)
            students = self.list_students(course_id, paginate_all=True)
            teachers = self.list_teachers(course_id, paginate_all=True)
            assignments = self.list_assignments(course_id, paginate_all=True)
            
            return {
                'course': course,
                'students': students,
                'teachers': teachers,
                'assignments': assignments,
                'stats': {
                    'student_count': len(students) if isinstance(students, list) else 0,
                    'teacher_count': len(teachers) if isinstance(teachers, list) else 0,
                    'assignment_count': len(assignments) if isinstance(assignments, list) else 0
                }
            }
            
        except Exception as e:
            self._handle_api_error(f"get course summary for {course_id}", e)


    def list_students(self, course_id: str, page_size: int = 100, 
                     paginate_all: bool = False) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        List students in a course.
        
        Args:
            course_id (str): Course ID
            page_size (int): Number of students to return per page
            paginate_all (bool): If True, return all results across all pages
            
        Returns:
            dict or list: Students data
        """
        try:
            if not course_id:
                raise ClassroomServiceError("Course ID is required")
            
            request_params = {
                'courseId': course_id,
                'pageSize': page_size
            }
            
            if paginate_all:
                return self._paginate_results(self.service.courses().students().list, **request_params)
            else:
                result = self.service.courses().students().list(**request_params).execute()
                return result
            
        except Exception as e:
            self._handle_api_error(f"list students for course {course_id}", e)

    def add_student(self, course_id: str, student_email: str) -> Dict[str, Any]:
        """
        Add a student to a course.
        
        Args:
            course_id (str): Course ID
            student_email (str): Student's email address
            
        Returns:
            dict: Student enrollment details
        """
        try:
            if not course_id or not student_email:
                raise ClassroomServiceError("Course ID and student email are required")
            
            # Validate email format (basic check)
            if '@' not in student_email:
                raise ClassroomServiceError("Invalid email format")
            
            student_body = {
                'userId': student_email
            }
            
            result = self.service.courses().students().create(
                courseId=course_id,
                body=student_body
            ).execute()
            
            logger.info(f"Successfully added student {student_email} to course {course_id}")
            return result
            
        except Exception as e:
            self._handle_api_error(f"add student {student_email} to course {course_id}", e)
        
    def bulk_add_students(self, course_id: str, student_emails: List[str]) -> Dict[str, Any]:
        """
        Add multiple students to a course.
        
        Args:
            course_id (str): Course ID
            student_emails (list): List of student email addresses
            
        Returns:
            dict: Results of bulk operation
        """
        results = {
            'successful': [],
            'failed': []
        }
        
        for email in student_emails:
            try:
                result = self.add_student(course_id, email)
                results['successful'].append({
                    'email': email,
                    'result': result
                })
            except Exception as e:
                results['failed'].append({
                    'email': email,
                    'error': str(e)
                })
        
        return results


    def remove_student(self, course_id: str, student_id: str) -> Dict[str, Any]:
        """
        Remove a student from a course.
        
        Args:
            course_id (str): Course ID
            student_id (str): Student ID or email
            
        Returns:
            dict: Empty response on success
        """
        try:
            result = self.service.courses().students().delete(
                courseId=course_id,
                userId=student_id
            ).execute()
            return result or {'success': True}
            
        except Exception as e:
            raise RuntimeError(f"Failed to remove student {student_id} from course {course_id}: {str(e)}")

    def list_teachers(self, course_id: str, page_size: int = 100) -> Dict[str, Any]:
        """
        List teachers in a course.
        
        Args:
            course_id (str): Course ID
            page_size (int): Number of teachers to return
            
        Returns:
            dict: Teachers data
        """
        try:
            result = self.service.courses().teachers().list(
                courseId=course_id,
                pageSize=page_size
            ).execute()
            return result
            
        except Exception as e:
            raise RuntimeError(f"Failed to list teachers for course {course_id}: {str(e)}")

    def add_teacher(self, course_id: str, teacher_email: str) -> Dict[str, Any]:
        """
        Add a teacher to a course.
        
        Args:
            course_id (str): Course ID
            teacher_email (str): Teacher's email address
            
        Returns:
            dict: Teacher enrollment details
        """
        try:
            teacher_body = {
                'userId': teacher_email
            }
            
            result = self.service.courses().teachers().create(
                courseId=course_id,
                body=teacher_body
            ).execute()
            return result
            
        except Exception as e:
            raise RuntimeError(f"Failed to add teacher {teacher_email} to course {course_id}: {str(e)}")

    def list_assignments(self, course_id: str, course_work_states: Optional[List[str]] = None, 
                        page_size: int = 100) -> Dict[str, Any]:
        """
        List assignments (coursework) in a course.
        
        Args:
            course_id (str): Course ID
            course_work_states (list, optional): Filter by coursework states
            page_size (int): Number of assignments to return
            
        Returns:
            dict: Assignments data
        """
        try:
            request_params = {
                'courseId': course_id,
                'pageSize': page_size
            }
            
            if course_work_states:
                request_params['courseWorkStates'] = course_work_states
            
            result = self.service.courses().courseWork().list(**request_params).execute()
            return result
            
        except Exception as e:
            raise RuntimeError(f"Failed to list assignments for course {course_id}: {str(e)}")

    def get_assignment(self, course_id: str, coursework_id: str) -> Dict[str, Any]:
        """
        Get details of a specific assignment.
        
        Args:
            course_id (str): Course ID
            coursework_id (str): Coursework/Assignment ID
            
        Returns:
            dict: Assignment details
        """
        try:
            result = self.service.courses().courseWork().get(
                courseId=course_id,
                id=coursework_id
            ).execute()
            return result
            
        except Exception as e:
            raise RuntimeError(f"Failed to get assignment {coursework_id}: {str(e)}")

    def list_submissions(self, course_id: str, coursework_id: str, user_id: Optional[str] = None,
                        states: Optional[List[str]] = None, page_size: int = 100) -> Dict[str, Any]:
        """
        List student submissions for an assignment.
        
        Args:
            course_id (str): Course ID
            coursework_id (str): Coursework/Assignment ID
            user_id (str, optional): Filter by user ID
            states (list, optional): Filter by submission states
            page_size (int): Number of submissions to return
            
        Returns:
            dict: Submissions data
        """
        try:
            request_params = {
                'courseId': course_id,
                'courseWorkId': coursework_id,
                'pageSize': page_size
            }
            
            if user_id:
                request_params['userId'] = user_id
            if states:
                request_params['states'] = states
            
            result = self.service.courses().courseWork().studentSubmissions().list(**request_params).execute()
            return result
            
        except Exception as e:
            raise RuntimeError(f"Failed to list submissions for assignment {coursework_id}: {str(e)}")

    def get_submission(self, course_id: str, coursework_id: str, submission_id: str) -> Dict[str, Any]:
        """
        Get details of a specific submission.
        
        Args:
            course_id (str): Course ID
            coursework_id (str): Coursework/Assignment ID
            submission_id (str): Submission ID
            
        Returns:
            dict: Submission details
        """
        try:
            result = self.service.courses().courseWork().studentSubmissions().get(
                courseId=course_id,
                courseWorkId=coursework_id,
                id=submission_id
            ).execute()
            return result
            
        except Exception as e:
            raise RuntimeError(f"Failed to get submission {submission_id}: {str(e)}")

    def create_assignment(self, course_id: str, title: str, description: Optional[str] = None,
                         due_date: Optional[str] = None, due_time: Optional[str] = None,
                         max_points: Optional[float] = None, work_type: str = "ASSIGNMENT") -> Dict[str, Any]:
        """
        Create a new assignment in Google Classroom.
        
        Args:
            course_id (str): Course ID
            title (str): Assignment title
            description (str, optional): Assignment description
            due_date (str, optional): Due date in YYYY-MM-DD format
            due_time (str, optional): Due time in HH:MM format
            max_points (float, optional): Maximum points
            work_type (str): Type of work (ASSIGNMENT, SHORT_ANSWER_QUESTION, MULTIPLE_CHOICE_QUESTION)
            
        Returns:
            dict: Created assignment details
        """
        try:
            coursework_body = {
                'title': title,
                'state': 'PUBLISHED',
                'workType': work_type
            }
            
            if description:
                coursework_body['description'] = description
            
            if max_points is not None:
                coursework_body['maxPoints'] = max_points
            
            # Handle due date and time
            if due_date:
                try:
                    # Parse date in YYYY-MM-DD format
                    if 'T' in due_date or 'Z' in due_date:
                        # ISO format
                        due_datetime = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                    else:
                        # Simple date format
                        due_datetime = datetime.strptime(due_date, '%Y-%m-%d')
                    
                    coursework_body['dueDate'] = {
                        'year': due_datetime.year,
                        'month': due_datetime.month,
                        'day': due_datetime.day
                    }
                    
                    if due_time:
                        time_parts = due_time.split(':')
                        coursework_body['dueTime'] = {
                            'hours': int(time_parts[0]),
                            'minutes': int(time_parts[1]) if len(time_parts) > 1 else 0
                        }
                except ValueError as e:
                    raise ValueError(f"Invalid date format. Use YYYY-MM-DD for date and HH:MM for time: {e}")
            
            result = self.service.courses().courseWork().create(
                courseId=course_id,
                body=coursework_body
            ).execute()
            return result
            
        except Exception as e:
            raise RuntimeError(f"Failed to create assignment: {str(e)}")

    def update_assignment(self, course_id: str, coursework_id: str, title: Optional[str] = None,
                         description: Optional[str] = None, due_date: Optional[str] = None,
                         due_time: Optional[str] = None, max_points: Optional[float] = None) -> Dict[str, Any]:
        """
        Update an existing assignment.
        
        Args:
            course_id (str): Course ID
            coursework_id (str): Coursework/Assignment ID
            title (str, optional): New title
            description (str, optional): New description
            due_date (str, optional): New due date in YYYY-MM-DD format
            due_time (str, optional): New due time in HH:MM format
            max_points (float, optional): New max points
            
        Returns:
            dict: Updated assignment details
        """
        try:
            # First get the existing assignment
            existing = self.get_assignment(course_id, coursework_id)
            
            update_mask = []
            
            # Update fields if provided
            if title is not None:
                existing['title'] = title
                update_mask.append('title')
            if description is not None:
                existing['description'] = description
                update_mask.append('description')
            if max_points is not None:
                existing['maxPoints'] = max_points
                update_mask.append('maxPoints')
            
            # Handle due date and time updates
            if due_date:
                try:
                    if 'T' in due_date or 'Z' in due_date:
                        due_datetime = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                    else:
                        due_datetime = datetime.strptime(due_date, '%Y-%m-%d')
                    
                    existing['dueDate'] = {
                        'year': due_datetime.year,
                        'month': due_datetime.month,
                        'day': due_datetime.day
                    }
                    update_mask.append('dueDate')
                    
                    if due_time:
                        time_parts = due_time.split(':')
                        existing['dueTime'] = {
                            'hours': int(time_parts[0]),
                            'minutes': int(time_parts[1]) if len(time_parts) > 1 else 0
                        }
                        update_mask.append('dueTime')
                except ValueError as e:
                    raise ValueError(f"Invalid date format. Use YYYY-MM-DD for date and HH:MM for time: {e}")
            
            if not update_mask:
                raise ValueError("No valid fields to update")
            
            result = self.service.courses().courseWork().patch(
                courseId=course_id,
                id=coursework_id,
                body=existing,
                updateMask=','.join(update_mask)
            ).execute()
            return result
            
        except Exception as e:
            raise RuntimeError(f"Failed to update assignment {coursework_id}: {str(e)}")

    def delete_assignment(self, course_id: str, coursework_id: str) -> Dict[str, Any]:
        """
        Delete an assignment.
        
        Args:
            course_id (str): Course ID
            coursework_id (str): Coursework/Assignment ID
            
        Returns:
            dict: Empty response on success
        """
        try:
            result = self.service.courses().courseWork().delete(
                courseId=course_id,
                id=coursework_id
            ).execute()
            return result or {'success': True}
            
        except Exception as e:
            raise RuntimeError(f"Failed to delete assignment {coursework_id}: {str(e)}")

    def grade_submission(self, course_id: str, coursework_id: str, submission_id: str,
                        assigned_grade: float, draft_grade: Optional[float] = None) -> Dict[str, Any]:
        """
        Grade a student submission.
        
        Args:
            course_id (str): Course ID
            coursework_id (str): Coursework/Assignment ID
            submission_id (str): Submission ID
            assigned_grade (float): Final grade to assign
            draft_grade (float, optional): Draft grade
            
        Returns:
            dict: Updated submission details
        """
        try:
            update_mask = ['assignedGrade']
            submission_body = {
                'assignedGrade': assigned_grade
            }
            
            if draft_grade is not None:
                submission_body['draftGrade'] = draft_grade
                update_mask.append('draftGrade')
            
            result = self.service.courses().courseWork().studentSubmissions().patch(
                courseId=course_id,
                courseWorkId=coursework_id,
                id=submission_id,
                body=submission_body,
                updateMask=','.join(update_mask)
            ).execute()
            return result
            
        except Exception as e:
            raise RuntimeError(f"Failed to grade submission {submission_id}: {str(e)}")

    def return_submission(self, course_id: str, coursework_id: str, submission_id: str) -> Dict[str, Any]:
        """
        Return a graded submission to the student.
        
        Args:
            course_id (str): Course ID
            coursework_id (str): Coursework/Assignment ID
            submission_id (str): Submission ID
            
        Returns:
            dict: Updated submission details
        """
        try:
            result = self.service.courses().courseWork().studentSubmissions().return_(
                courseId=course_id,
                courseWorkId=coursework_id,
                id=submission_id,
                body={}
            ).execute()
            return result
            
        except Exception as e:
            raise RuntimeError(f"Failed to return submission {submission_id}: {str(e)}")

    def list_announcements(self, course_id: str, page_size: int = 100) -> Dict[str, Any]:
        """
        List announcements in a course.
        
        Args:
            course_id (str): Course ID
            page_size (int): Number of announcements to return
            
        Returns:
            dict: Announcements data
        """
        try:
            result = self.service.courses().announcements().list(
                courseId=course_id,
                pageSize=page_size
            ).execute()
            return result
            
        except Exception as e:
            raise RuntimeError(f"Failed to list announcements for course {course_id}: {str(e)}")

    def create_announcement(self, course_id: str, text: str, state: str = "PUBLISHED") -> Dict[str, Any]:
        """
        Create a new announcement in Google Classroom.
        
        Args:
            course_id (str): Course ID
            text (str): Announcement text
            state (str): Announcement state (PUBLISHED, DRAFT)
            
        Returns:
            dict: Created announcement details
        """
        try:
            announcement_body = {
                'text': text,
                'state': state
            }
            
            result = self.service.courses().announcements().create(
                courseId=course_id,
                body=announcement_body
            ).execute()
            return result
            
        except Exception as e:
            raise RuntimeError(f"Failed to create announcement: {str(e)}")

    def update_announcement(self, course_id: str, announcement_id: str, text: Optional[str] = None,
                           state: Optional[str] = None) -> Dict[str, Any]:
        """
        Update an existing announcement.
        
        Args:
            course_id (str): Course ID
            announcement_id (str): Announcement ID
            text (str, optional): New announcement text
            state (str, optional): New announcement state
            
        Returns:
            dict: Updated announcement details
        """
        try:
            # Get existing announcement
            existing = self.service.courses().announcements().get(
                courseId=course_id,
                id=announcement_id
            ).execute()
            
            update_mask = []
            
            if text is not None:
                existing['text'] = text
                update_mask.append('text')
            if state is not None:
                existing['state'] = state
                update_mask.append('state')
            
            if not update_mask:
                raise ValueError("No valid fields to update")
            
            result = self.service.courses().announcements().patch(
                courseId=course_id,
                id=announcement_id,
                body=existing,
                updateMask=','.join(update_mask)
            ).execute()
            return result
            
        except Exception as e:
            raise RuntimeError(f"Failed to update announcement {announcement_id}: {str(e)}")

    def delete_announcement(self, course_id: str, announcement_id: str) -> Dict[str, Any]:
        """
        Delete an announcement.
        
        Args:
            course_id (str): Course ID
            announcement_id (str): Announcement ID
            
        Returns:
            dict: Empty response on success
        """
        try:
            result = self.service.courses().announcements().delete(
                courseId=course_id,
                id=announcement_id
            ).execute()
            return result or {'success': True}
            
        except Exception as e:
            raise RuntimeError(f"Failed to delete announcement {announcement_id}: {str(e)}")

    def get_user_profile(self, user_id: str = "me") -> Dict[str, Any]:
        """
        Get user profile information.
        
        Args:
            user_id (str): User ID (defaults to "me" for current user)
            
        Returns:
            dict: User profile data
        """
        try:
            result = self.service.userProfiles().get(userId=user_id).execute()
            return result
            
        except Exception as e:
            raise RuntimeError(f"Failed to get user profile: {str(e)}")

    def get_guardian_invitations(self, student_id: str, page_size: int = 100) -> Dict[str, Any]:
        """
        Get guardian invitations for a student.
        
        Args:
            student_id (str): Student ID
            page_size (int): Number of invitations to return
            
        Returns:
            dict: Guardian invitations data
        """
        try:
            result = self.service.userProfiles().guardianInvitations().list(
                studentId=student_id,
                pageSize=page_size
            ).execute()
            return result
            
        except Exception as e:
            raise RuntimeError(f"Failed to get guardian invitations for student {student_id}: {str(e)}")

    def invite_guardian(self, student_id: str, guardian_email: str) -> Dict[str, Any]:
        """
        Invite a guardian for a student.
        
        Args:
            student_id (str): Student ID
            guardian_email (str): Guardian's email address
            
        Returns:
            dict: Guardian invitation details
        """
        try:
            invitation_body = {
                'studentId': student_id,
                'invitedEmailAddress': guardian_email
            }
            
            result = self.service.userProfiles().guardianInvitations().create(
                studentId=student_id,
                body=invitation_body
            ).execute()
            return result
            
        except Exception as e:
            raise RuntimeError(f"Failed to invite guardian {guardian_email} for student {student_id}: {str(e)}")