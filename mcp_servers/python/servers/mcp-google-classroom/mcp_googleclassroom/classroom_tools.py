from collections.abc import Sequence
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from . import classroom_service
import json
from . import toolhandler

class ListCoursesToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("list_classroom_courses")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="List all courses in Google Classroom.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "teacher_id": {
                        "type": "string",
                        "description": "Filter courses by teacher ID (optional)"
                    },
                    "student_id": {
                        "type": "string",
                        "description": "Filter courses by student ID (optional)"
                    },
                    "course_states": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter courses by state (ACTIVE, ARCHIVED, PROVISIONED, DECLINED, SUSPENDED)"
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Number of courses to return (default: 100)",
                        "default": 100
                    }
                },
                "required": []
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        
        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.list_courses(
            teacher_id=args.get('teacher_id'),
            student_id=args.get('student_id'),
            course_states=args.get('course_states'),
            page_size=args.get('page_size', 100)
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class GetCourseToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("get_classroom_course")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get details of a specific course in Google Classroom.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    }
                },
                "required": ["course_id"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        course_id = args.get('course_id')
        
        if not course_id:
            raise RuntimeError("Missing required argument: course_id")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.get_course(course_id)

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class ListStudentsToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("list_classroom_students")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="List students in a specific course.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Number of students to return (default: 100)",
                        "default": 100
                    }
                },
                "required": ["course_id"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        course_id = args.get('course_id')
        
        if not course_id:
            raise RuntimeError("Missing required argument: course_id")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.list_students(
            course_id=course_id,
            page_size=args.get('page_size', 100)
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class ListAssignmentsToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("list_classroom_assignments")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="List assignments (coursework) in a specific course.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    },
                    "course_work_states": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter assignments by state (PUBLISHED, DRAFT, DELETED)"
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Number of assignments to return (default: 100)",
                        "default": 100
                    }
                },
                "required": ["course_id"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        course_id = args.get('course_id')
        
        if not course_id:
            raise RuntimeError("Missing required argument: course_id")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.list_assignments(
            course_id=course_id,
            course_work_states=args.get('course_work_states'),
            page_size=args.get('page_size', 100)
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class GetAssignmentToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("get_classroom_assignment")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get details of a specific assignment.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    },
                    "coursework_id": {
                        "type": "string",
                        "description": "Coursework/Assignment ID"
                    }
                },
                "required": ["course_id", "coursework_id"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        course_id = args.get('course_id')
        coursework_id = args.get('coursework_id')
        
        if not course_id or not coursework_id:
            raise RuntimeError("Missing required arguments: course_id and coursework_id")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.get_assignment(
            course_id=course_id,
            coursework_id=coursework_id
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class ListSubmissionsToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("list_classroom_submissions")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="List student submissions for a specific assignment.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    },
                    "coursework_id": {
                        "type": "string",
                        "description": "Coursework/Assignment ID"
                    },
                    "user_id": {
                        "type": "string",
                        "description": "Filter submissions by user ID (optional)"
                    },
                    "states": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter submissions by state (NEW, CREATED, TURNED_IN, RETURNED, RECLAIMED_BY_STUDENT)"
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Number of submissions to return (default: 100)",
                        "default": 100
                    }
                },
                "required": ["course_id", "coursework_id"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        course_id = args.get('course_id')
        coursework_id = args.get('coursework_id')
        
        if not course_id or not coursework_id:
            raise RuntimeError("Missing required arguments: course_id and coursework_id")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.list_submissions(
            course_id=course_id,
            coursework_id=coursework_id,
            user_id=args.get('user_id'),
            states=args.get('states'),
            page_size=args.get('page_size', 100)
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class CreateAssignmentToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("create_classroom_assignment")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Create a new assignment in Google Classroom.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    },
                    "title": {
                        "type": "string",
                        "description": "Assignment title"
                    },
                    "description": {
                        "type": "string",
                        "description": "Assignment description (optional)"
                    },
                    "due_date": {
                        "type": "string",
                        "description": "Due date in ISO format (optional)"
                    },
                    "due_time": {
                        "type": "string",
                        "description": "Due time in HH:MM format (optional)"
                    },
                    "max_points": {
                        "type": "number",
                        "description": "Maximum points for the assignment (optional)"
                    },
                    "work_type": {
                        "type": "string",
                        "description": "Type of work (ASSIGNMENT, SHORT_ANSWER_QUESTION, MULTIPLE_CHOICE_QUESTION)"
                    }
                },
                "required": ["course_id", "title", "work_type"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        course_id = args.get('course_id')
        title = args.get('title')
        work_type = args.get('work_type')
        
        if not course_id or not title or not work_type:
            raise RuntimeError("Missing required arguments: course_id, title, and work_type")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.create_assignment(
            course_id=course_id,
            title=title,
            description=args.get('description'),
            due_date=args.get('due_date'),
            due_time=args.get('due_time'),
            max_points=args.get('max_points'),
            work_type=work_type
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class GradeSubmissionToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("grade_classroom_submission")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Grade a student submission in Google Classroom.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    },
                    "coursework_id": {
                        "type": "string",
                        "description": "Coursework/Assignment ID"
                    },
                    "submission_id": {
                        "type": "string",
                        "description": "Submission ID"
                    },
                    "assigned_grade": {
                        "type": "number",
                        "description": "Final grade to assign"
                    },
                    "draft_grade": {
                        "type": "number",
                        "description": "Draft grade (optional)"
                    }
                },
                "required": ["course_id", "coursework_id", "submission_id", "assigned_grade"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        course_id = args.get('course_id')
        coursework_id = args.get('coursework_id')
        submission_id = args.get('submission_id')
        assigned_grade = args.get('assigned_grade')
        
        if not all([course_id, coursework_id, submission_id, assigned_grade is not None]):
            raise RuntimeError("Missing required arguments: course_id, coursework_id, submission_id, and assigned_grade")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.grade_submission(
            course_id=course_id,
            coursework_id=coursework_id,
            submission_id=submission_id,
            assigned_grade=assigned_grade,
            draft_grade=args.get('draft_grade')
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class ListAnnouncementsToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("list_classroom_announcements")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="List announcements in a Google Classroom course.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Number of announcements to return (default: 100)",
                        "default": 100
                    }
                },
                "required": ["course_id"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        course_id = args.get('course_id')
        
        if not course_id:
            raise RuntimeError("Missing required argument: course_id")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.list_announcements(
            course_id=course_id,
            page_size=args.get('page_size', 100)
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class CreateAnnouncementToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("create_classroom_announcement")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Create a new announcement in Google Classroom.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    },
                    "text": {
                        "type": "string",
                        "description": "Announcement text"
                    },
                    "state": {
                        "type": "string",
                        "description": "Announcement state (PUBLISHED, DRAFT)",
                        "default": "PUBLISHED"
                    }
                },
                "required": ["course_id", "text"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        course_id = args.get('course_id')
        text = args.get('text')
        
        if not course_id or not text:
            raise RuntimeError("Missing required arguments: course_id and text")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.create_announcement(
            course_id=course_id,
            text=text,
            state=args.get('state', 'PUBLISHED')
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class GetUserProfileToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("get_classroom_user_profile")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get user profile information from Google Classroom.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "user_id": {
                        "type": "string",
                        "description": "User ID (defaults to 'me' for current user)",
                        "default": "me"
                    }
                },
                "required": []
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.get_user_profile(
            user_id=args.get('user_id', 'me')
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

# Add this to classroom_tools.py

class ListTeachersToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("list_classroom_teachers")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="List teachers in a specific course.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Number of teachers to return (default: 100)",
                        "default": 100
                    }
                },
                "required": ["course_id"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        course_id = args.get('course_id')
        
        if not course_id:
            raise RuntimeError("Missing required argument: course_id")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.list_teachers(
            course_id=course_id,
            page_size=args.get('page_size', 100)
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class CreateCourseToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("create_classroom_course")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Create a new course in Google Classroom.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "name": {
                        "type": "string",
                        "description": "Name of the course (required)"
                    },
                    "section": {
                        "type": "string",
                        "description": "Section name (optional)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Course description (optional)"
                    },
                    "description_heading": {
                        "type": "string",
                        "description": "Description heading (optional)"
                    },
                    "room": {
                        "type": "string",
                        "description": "Room location (optional)"
                    },
                    "owner_id": {
                        "type": "string",
                        "description": "Owner identifier (default: 'me')",
                        "default": "me"
                    },
                    "course_state": {
                        "type": "string",
                        "description": "Course state (default: 'ACTIVE')",
                        "default": "ACTIVE"
                    }
                },
                "required": ["name"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        name = args.get('name')
        
        if not name:
            raise RuntimeError("Missing required argument: name")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.create_course(
            name=name,
            section=args.get('section'),
            description=args.get('description'),
            description_heading=args.get('description_heading'),
            room=args.get('room'),
            owner_id=args.get('owner_id', 'me'),
            course_state=args.get('course_state', 'ACTIVE')
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class UpdateCourseToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("update_classroom_course")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Update an existing course in Google Classroom.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    },
                    "name": {
                        "type": "string",
                        "description": "New name (optional)"
                    },
                    "section": {
                        "type": "string",
                        "description": "New section (optional)"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description (optional)"
                    },
                    "description_heading": {
                        "type": "string",
                        "description": "New description heading (optional)"
                    },
                    "room": {
                        "type": "string",
                        "description": "New room (optional)"
                    },
                    "course_state": {
                        "type": "string",
                        "description": "New course state (optional)"
                    },
                    "owner_id": {
                        "type": "string",
                        "description": "New owner (optional)"
                    }
                },
                "required": ["course_id"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        course_id = args.get('course_id')
        
        if not course_id:
            raise RuntimeError("Missing required argument: course_id")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.update_course(
            course_id=course_id,
            name=args.get('name'),
            section=args.get('section'),
            description=args.get('description'),
            description_heading=args.get('description_heading'),
            room=args.get('room'),
            course_state=args.get('course_state'),
            owner_id=args.get('owner_id')
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class DeleteCourseToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("delete_classroom_course")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Archive a course in Google Classroom (courses cannot be permanently deleted).",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    }
                },
                "required": ["course_id"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        course_id = args.get('course_id')
        
        if not course_id:
            raise RuntimeError("Missing required argument: course_id")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.delete_course(course_id)

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class GetCourseSummaryToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("get_classroom_course_summary")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get a comprehensive summary of a course including students, teachers, and assignments.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    }
                },
                "required": ["course_id"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        course_id = args.get('course_id')
        
        if not course_id:
            raise RuntimeError("Missing required argument: course_id")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.get_course_summary(course_id)

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class AddStudentToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("add_classroom_student")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Add a student to a course in Google Classroom.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    },
                    "student_email": {
                        "type": "string",
                        "description": "Student's email address"
                    }
                },
                "required": ["course_id", "student_email"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        course_id = args.get('course_id')
        student_email = args.get('student_email')
        
        if not course_id or not student_email:
            raise RuntimeError("Missing required arguments: course_id and student_email")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.add_student(
            course_id=course_id,
            student_email=student_email
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class BulkAddStudentsToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("bulk_add_classroom_students")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Add multiple students to a course in Google Classroom.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    },
                    "student_emails": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of student email addresses"
                    }
                },
                "required": ["course_id", "student_emails"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        course_id = args.get('course_id')
        student_emails = args.get('student_emails')
        
        if not course_id or not student_emails:
            raise RuntimeError("Missing required arguments: course_id and student_emails")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.bulk_add_students(
            course_id=course_id,
            student_emails=student_emails
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class RemoveStudentToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("remove_classroom_student")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Remove a student from a course in Google Classroom.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    },
                    "student_id": {
                        "type": "string",
                        "description": "Student ID or email"
                    }
                },
                "required": ["course_id", "student_id"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        course_id = args.get('course_id')
        student_id = args.get('student_id')
        
        if not course_id or not student_id:
            raise RuntimeError("Missing required arguments: course_id and student_id")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.remove_student(
            course_id=course_id,
            student_id=student_id
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class AddTeacherToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("add_classroom_teacher")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Add a teacher to a course in Google Classroom.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    },
                    "teacher_email": {
                        "type": "string",
                        "description": "Teacher's email address"
                    }
                },
                "required": ["course_id", "teacher_email"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        course_id = args.get('course_id')
        teacher_email = args.get('teacher_email')
        
        if not course_id or not teacher_email:
            raise RuntimeError("Missing required arguments: course_id and teacher_email")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.add_teacher(
            course_id=course_id,
            teacher_email=teacher_email
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class GetSubmissionToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("get_classroom_submission")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get details of a specific student submission.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    },
                    "coursework_id": {
                        "type": "string",
                        "description": "Coursework/Assignment ID"
                    },
                    "submission_id": {
                        "type": "string",
                        "description": "Submission ID"
                    }
                },
                "required": ["course_id", "coursework_id", "submission_id"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        course_id = args.get('course_id')
        coursework_id = args.get('coursework_id')
        submission_id = args.get('submission_id')
        
        if not all([course_id, coursework_id, submission_id]):
            raise RuntimeError("Missing required arguments: course_id, coursework_id, and submission_id")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.get_submission(
            course_id=course_id,
            coursework_id=coursework_id,
            submission_id=submission_id
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class UpdateAssignmentToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("update_classroom_assignment")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Update an existing assignment in Google Classroom.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    },
                    "coursework_id": {
                        "type": "string",
                        "description": "Coursework/Assignment ID"
                    },
                    "title": {
                        "type": "string",
                        "description": "New title (optional)"
                    },
                    "description": {
                        "type": "string",
                        "description": "New description (optional)"
                    },
                    "due_date": {
                        "type": "string",
                        "description": "New due date in YYYY-MM-DD format (optional)"
                    },
                    "due_time": {
                        "type": "string",
                        "description": "New due time in HH:MM format (optional)"
                    },
                    "max_points": {
                        "type": "number",
                        "description": "New max points (optional)"
                    }
                },
                "required": ["course_id", "coursework_id"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        course_id = args.get('course_id')
        coursework_id = args.get('coursework_id')
        
        if not course_id or not coursework_id:
            raise RuntimeError("Missing required arguments: course_id and coursework_id")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.update_assignment(
            course_id=course_id,
            coursework_id=coursework_id,
            title=args.get('title'),
            description=args.get('description'),
            due_date=args.get('due_date'),
            due_time=args.get('due_time'),
            max_points=args.get('max_points')
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class DeleteAssignmentToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("delete_classroom_assignment")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Delete an assignment in Google Classroom.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    },
                    "coursework_id": {
                        "type": "string",
                        "description": "Coursework/Assignment ID"
                    }
                },
                "required": ["course_id", "coursework_id"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        course_id = args.get('course_id')
        coursework_id = args.get('coursework_id')
        
        if not course_id or not coursework_id:
            raise RuntimeError("Missing required arguments: course_id and coursework_id")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.delete_assignment(
            course_id=course_id,
            coursework_id=coursework_id
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class ReturnSubmissionToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("return_classroom_submission")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Return a graded submission to the student.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    },
                    "coursework_id": {
                        "type": "string",
                        "description": "Coursework/Assignment ID"
                    },
                    "submission_id": {
                        "type": "string",
                        "description": "Submission ID"
                    }
                },
                "required": ["course_id", "coursework_id", "submission_id"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        course_id = args.get('course_id')
        coursework_id = args.get('coursework_id')
        submission_id = args.get('submission_id')
        
        if not all([course_id, coursework_id, submission_id]):
            raise RuntimeError("Missing required arguments: course_id, coursework_id, and submission_id")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.return_submission(
            course_id=course_id,
            coursework_id=coursework_id,
            submission_id=submission_id
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class UpdateAnnouncementToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("update_classroom_announcement")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Update an existing announcement in Google Classroom.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    },
                    "announcement_id": {
                        "type": "string",
                        "description": "Announcement ID"
                    },
                    "text": {
                        "type": "string",
                        "description": "New announcement text (optional)"
                    },
                    "state": {
                        "type": "string",
                        "description": "New announcement state (optional)"
                    }
                },
                "required": ["course_id", "announcement_id"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        course_id = args.get('course_id')
        announcement_id = args.get('announcement_id')
        
        if not course_id or not announcement_id:
            raise RuntimeError("Missing required arguments: course_id and announcement_id")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.update_announcement(
            course_id=course_id,
            announcement_id=announcement_id,
            text=args.get('text'),
            state=args.get('state')
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class DeleteAnnouncementToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("delete_classroom_announcement")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Delete an announcement in Google Classroom.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "course_id": {
                        "type": "string",
                        "description": "Course ID"
                    },
                    "announcement_id": {
                        "type": "string",
                        "description": "Announcement ID"
                    }
                },
                "required": ["course_id", "announcement_id"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        course_id = args.get('course_id')
        announcement_id = args.get('announcement_id')
        
        if not course_id or not announcement_id:
            raise RuntimeError("Missing required arguments: course_id and announcement_id")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.delete_announcement(
            course_id=course_id,
            announcement_id=announcement_id
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class GetGuardianInvitationsToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("get_classroom_guardian_invitations")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Get guardian invitations for a student.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "student_id": {
                        "type": "string",
                        "description": "Student ID"
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "Number of invitations to return (default: 100)",
                        "default": 100
                    }
                },
                "required": ["student_id"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        student_id = args.get('student_id')
        
        if not student_id:
            raise RuntimeError("Missing required argument: student_id")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.get_guardian_invitations(
            student_id=student_id,
            page_size=args.get('page_size', 100)
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]

class InviteGuardianToolHandler(toolhandler.ToolHandler):
    def __init__(self):
        super().__init__("invite_classroom_guardian")

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description="Invite a guardian for a student.",
            inputSchema={
                "type": "object",
                "properties": {
                    toolhandler.CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    toolhandler.SERVER_CREDENTIALS_ARG: self.get_credentials_arg_schema(),
                    "student_id": {
                        "type": "string",
                        "description": "Student ID"
                    },
                    "guardian_email": {
                        "type": "string",
                        "description": "Guardian's email address"
                    }
                },
                "required": ["student_id", "guardian_email"]
            }
        )

    def run_tool(self, args: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        credentials = self.extract_classroom_credentials(args)
        student_id = args.get('student_id')
        guardian_email = args.get('guardian_email')
        
        if not student_id or not guardian_email:
            raise RuntimeError("Missing required arguments: student_id and guardian_email")

        classroom_service_instance = classroom_service.ClassroomService(credentials)
        
        result = classroom_service_instance.invite_guardian(
            student_id=student_id,
            guardian_email=guardian_email
        )

        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )
        ]
