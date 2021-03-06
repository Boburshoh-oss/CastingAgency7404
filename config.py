
import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True
# token
EXECUTIVE_PRODUCER = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkhxeEJXY180aU1jWG9EWTA2REotRiJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLTc0MDQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxMTc4ZDYwODFkOTliMDA3MGVmNWE3NCIsImF1ZCI6ImNhcHN0b25lLWFwaSIsImlhdCI6MTYyOTEwNzE4NCwiZXhwIjoxNjI5MTkzNTg0LCJhenAiOiJQU1J3MTROU2dQb1dpSXFMM3A0UjU2czJsY3JFM2UxbiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9ycyIsImNyZWF0ZTptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwidXBkYXRlOmFjdG9ycyIsInVwZGF0ZTptb3ZpZXMiXX0.srzkyYGxQa6EMx496ZVvpSUwq-OPUrchEAbG3h8lZHyRIff2874XfX5UmY7vLxS1NyAQ9Pt48G-1SAeYtNk8gqkbZ866x_ewJEKGyVJMONgXTiX9gI24QLP0is9-nHAn-sXwoG-hTnOFfgBzDiQ6n4rTXyiwHae4Qfj0Z6Fm9gqmcq4VoJptt7FoFY1fXHzAZ12rUVPyq7HgQDB9t6_nZ3I5BrQq0wZNmSg81CH8ybP6XSxVA0VQq6GN5EaOHwhilzrv8u4vC2ZHtm1vIiXgxPOitrOPKimp3KpnLPZx_U0XD65rkChExDueO1PmAYNJqLG2dtpKpp7KrIHuWG7PLw"
CASTING_ASSISTANT = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkhxeEJXY180aU1jWG9EWTA2REotRiJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLTc0MDQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxMTdmNTA5NTIwOTY2MDA3MDdhOGZiZSIsImF1ZCI6ImNhcHN0b25lLWFwaSIsImlhdCI6MTYyOTExMTk5NSwiZXhwIjoxNjI5MTk4Mzk1LCJhenAiOiJQU1J3MTROU2dQb1dpSXFMM3A0UjU2czJsY3JFM2UxbiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.ZNYaOZslk_R6qmtBa48n4fn8pp7KP6lPsm_f6bm7CPinzamUQ2iTVX6wrTvRQdYIDjjhcpFDXnHSV8R298Hkcude09Og7g4Yld5ki2uhDiFMPdSCrl3-8vsumTnY_uZnN3yssh57udYHo197DlHdqm1xuvAje5jXxEtbBqqweUxIFfk_TyF8xxV1EGDORAXMyyPVCgA1eNmR65YFsHNCLOjkbLag-GmC7OiWR7XAgnZsky3lZHROgEHvvKHKOV-KjoG9KwsQv7mACTmkledy5AgaOv2vqyb_Ej-jqHBVQ9G-A_a-ot5_5z7cYpeNiKypjqnP5ccOR6OR28jZN3sITw"
CASTING_DIRECTOR = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkhxeEJXY180aU1jWG9EWTA2REotRiJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLTc0MDQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxMTdmM2RiMjAxYzJlMDA2OTg1NjVkYyIsImF1ZCI6ImNhcHN0b25lLWFwaSIsImlhdCI6MTYyOTExMTg4NSwiZXhwIjoxNjI5MTk4Mjg1LCJhenAiOiJQU1J3MTROU2dQb1dpSXFMM3A0UjU2czJsY3JFM2UxbiIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInVwZGF0ZTphY3RvcnMiLCJ1cGRhdGU6bW92aWVzIl19.nt_paKjFXbY1TNbZUVwDD6ni1eaiMySOBurSKPnGOJ51tAaUbUWXZiIcE9FUJZGcJEkL4Pi_w8uXjMqNnw3cqWJv7j5waUsXK_5At8W8qd9Kfd8Qi0J0_bRq3n1dM3Ya5FzdIIvJ-MyRlk3yw0ZSbovx5TUz3p2LvVfjaPj_ZJfgmUY4w7qSBT1L1DC9wsToqWL2wZ7owLxAL2eIUiTVVCNI1gpOw8fegK4OluCdN73mmRuwC-6Iq1wHP8Vc94kAD9scjr5yxVY-rq2YLp7YAmHIOh1d-jXqsBk0ELQ-YVS4DFzNMG77i5mDCAk1ePiLTh-LHE1Dsj_FkXDovYGa9A"

# Connect to the database
database_param = {
    "username": "postgres",
    "password": "admin",
    "db_name": "capstone",
    "dialect": "postgresql"
}
