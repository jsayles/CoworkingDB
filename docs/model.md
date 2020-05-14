# CRDB Data Models

Person
 - first_name
 - last_name
 - emails:  A list of emails for this person
 - description:  A bio for this person
 - websites:  A list of websites for this person
 - location:  Physical location if available
 - phone:  Contact phone number
 - gender
 - pronouns

Project
 - name
 - code:  A unique code for identification
 - description
 - type
    - SPACE
    - VENDOR
    - CONSULTANT
    - NONPROFIT
    - COOP
    - COLLECTIVE
    - OTHER
 - websites:  List of websites for the project
 - email: Contact email for the project
 - phone:  Contact phone number
 - location:  Physical location
 - start_month:  The month the project started
 - start_year:  The year the project started (required)
 - end_month:  The ending month if project is completed
 - end_year:  The ending year if the project is completed
 - created_ts:  Timestamp when project was created
 - created_by:  Person who created this project entry
 - updated_ts:  Timestamp when project was last updated
 - updated_by:  Person who last updated this project
 - is_flagged

PersonalRelationship
 - person
 - relationship

ProjectRelationship
 - related_project
 - relationship

Relationship
 - project: The project this relationship is with
 - start_month:  The month this relationship started
 - start_year:  The year this relationship started (required)
 - end_month:  The ending month if this relationship is over
 - end_year:  The ending year if this relationship is over
 - type
    - FOUNDER
    - OWNER
    - EMPLOYEE
    - MEMBER
    - VOLUNTEER
    - WORKTRADE
    - BOARD
    - VENDOR
    - CONSULT
    - OTHER
