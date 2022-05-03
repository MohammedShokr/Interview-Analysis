import sqlite3
conn = sqlite3.connect('company_data.db', check_same_thread=False)
conn.execute('PRAGMA foreign_keys = 3')
c = conn.cursor()


def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS company
               (
                comp_ID     text    PRIMARY KEY,
                comp_name   text,
                website     text
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS job
               (
                job_ID          text     PRIMARY KEY,
                job_title       text,
                job_req         text,
                job_description text,
                comp_ID         text,
                FOREIGN KEY (comp_ID) REFERENCES company (comp_ID)
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS candidate
               (
                cand_ID             real    PRIMARY KEY,
                cand_name           text,
                cand_qualifications text
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS analysis
               (
                cand_ID             real,
                job_ID              text,
                question_no         real,
                FER                 text,
                FER_score           real,
                tone                text,
                tone_score          text,
                coherence_score     real,
                pronunciation_score real,
                fluency_score       real,
                PRIMARY KEY (cand_ID, job_ID),
                FOREIGN KEY (cand_ID) REFERENCES candidate (cand_ID),
                FOREIGN KEY (job_ID) REFERENCES job (job_ID)
                )''')
    conn.commit()

def add_analysis(cand_ID, job_ID, question_no, FER , FER_score, tone, tone_score,coherence_score, pronunciation_score, fluency_score):
    c.execute('''INSERT INTO analysis(cand_ID, job_ID, question_no, FER , FER_score, tone, tone_score,coherence_score, pronunciation_score, fluency_score)
                 VALUES (?,?,?,?,?,?,?,?,?,?)''', (cand_ID, job_ID, question_no, FER , FER_score, tone, tone_score,coherence_score, pronunciation_score, fluency_score))
    conn.commit()

def add_company(comp_ID, comp_name, website):
    c.execute('''INSERT INTO company(comp_ID, comp_name, website)
                 VALUES (?,?,?)''', (comp_ID, comp_name, website))
    conn.commit()

def add_job(job_ID, job_title, job_req, job_description, comp_ID):
    c.execute('''INSERT INTO job(job_ID, job_title, job_req, job_description, comp_ID)
                 VALUES (?,?,?,?,?)''', (job_ID, job_title, job_req, job_description, comp_ID))
    conn.commit()

def add_candidate(cand_ID, cand_name, cand_qualifications):
    c.execute('''INSERT INTO candidate(cand_ID, cand_name, cand_qualifications)
                 VALUES (?,?,?)''', (cand_ID, cand_name, cand_qualifications))
    conn.commit()

def view_analysis_data():
    c.execute('SELECT * FROM analysis')
    data = c.fetchall()
    return data

def view_company_data():
    c.execute('SELECT * FROM company')
    data = c.fetchall()
    return data

def view_job_data():
    c.execute('SELECT * FROM job')
    data = c.fetchall()
    return data

def view_candidate_data():
    c.execute('SELECT * FROM candidate')
    data = c.fetchall()
    return data

def view_schema():
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return c.fetchall()

def get_cand(cand_id):
	c.execute('SELECT * FROM candidate WHERE cand_id="{}"'.format(cand_id))
	data = c.fetchall()
	return data

def get_job(job_id):
    c.execute('SELECT * FROM job WHERE job_id="{}"'.format(job_id))
    data = c.fetchall()
    return data

def get_analysis_with_job(job_id):
    c.execute('SELECT * FROM analysis WHERE job_id="{}"'.format(job_id))
    data = c.fetchall()
    return data

def get_analysis_with_cand(cand_id):
    c.execute('SELECT * FROM analysis WHERE cand_id="{}"'.format(cand_id))
    data = c.fetchall()
    return data