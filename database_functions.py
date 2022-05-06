import sqlite3
conn = sqlite3.connect('database.db', check_same_thread=False)
conn.execute('PRAGMA foreign_keys = 3')
c = conn.cursor()


def create_tables():
    c.execute("DROP TABLE analysis")
    c.execute('''CREATE TABLE IF NOT EXISTS company
               (
                comp_ID     text    PRIMARY KEY,
                comp_name   text,
                comp_pass   text,
                website     text
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS job
               (
                job_title       text,
                job_req         text,
                job_description text,
                comp_ID         text,
                PRIMARY KEY (comp_ID, job_title),
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
                cand_ID             text,
                comp_ID             text,
                job_title           text,
                interview_no        NUM,
                question_no         NUM,
                FER                 text,
                FER_score           real,
                tone                text,
                tone_score          real, 
                fluency             text,
                fluency_score       real,
                coherence_score     real,
                overall_score       real,
                FOREIGN KEY (cand_ID) REFERENCES candidate (cand_ID),
                FOREIGN KEY (comp_ID,job_title) REFERENCES job (comp_ID,job_title)
                )''')
    conn.commit()

def add_analysis(cand_ID, comp_ID, job_title, interview_no, question_no, FER , FER_score, tone, tone_score, fluency, fluency_score, coherence_score, overall_score):
    c.execute('''INSERT INTO analysis(cand_ID, comp_ID, job_title, interview_no, question_no, FER , FER_score, tone, tone_score, fluency, fluency_score, coherence_score, overall_score)
                 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', (cand_ID, comp_ID, job_title, interview_no, question_no, FER , FER_score, tone, tone_score, fluency, fluency_score, coherence_score, overall_score))
    conn.commit()

def add_company(comp_ID, comp_name, comp_pass, website):
    c.execute('''INSERT INTO company(comp_ID, comp_name, comp_pass, website)
                 VALUES (?,?,?,?)''', (comp_ID, comp_name, comp_pass, website))
    conn.commit()

def add_job(job_title, job_req, job_description, comp_ID):
    c.execute('''INSERT INTO job(job_title, job_req, job_description, comp_ID)
                 VALUES (?,?,?,?)''', (job_title, job_req, job_description, comp_ID))
    conn.commit()

def add_candidate(cand_ID, cand_name, cand_qualifications):
    c.execute('''INSERT INTO candidate(cand_ID, cand_name, cand_qualifications)
                 VALUES (?,?,?)''', (cand_ID, cand_name, cand_qualifications))
    conn.commit()

def delete_one_analysis(cand_ID, comp_ID, job_title, interview_no, question_no):
    c.execute('''DELETE FROM analysis WHERE cand_ID=? AND comp_ID=? AND job_title=? AND 
              interview_no=? AND question_no=?''', (cand_ID, comp_ID, job_title, interview_no, question_no))
    conn.commit()
    
def delete_analysis_cand(cand_ID):
    c.execute('''DELETE FROM analysis WHERE cand_ID=? ''', (cand_ID))
    conn.commit()
    
def delete_analysis_job(comp_ID, job_title):
    c.execute('''DELETE FROM analysis WHERE comp_ID=? AND job_title=?''', (comp_ID, job_title))
    conn.commit()
    
def delete_analysis_cand_job(cand_ID, comp_ID, job_title):
    c.execute('''DELETE FROM analysis WHERE cand_ID=? AND comp_ID=? AND job_title=?
              ''', (cand_ID, comp_ID, job_title))
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

def get_jobs_comp(comp_id):
    c.execute('SELECT * FROM job WHERE comp_ID="{}"'.format(comp_id))
    data = c.fetchall()
    return data

def get_analysis_with_job(comp_id, job_title):
    c.execute('SELECT * FROM analysis WHERE comp_ID=? AND job_title=?',(comp_id, job_title))
    data = c.fetchall()
    return data

def get_analysis_with_cand(cand_id):
    c.execute('SELECT * FROM analysis WHERE cand_ID="{}"'.format(cand_id))
    data = c.fetchall()
    return data

def get_analysis_with_job_cand(comp_id, job_title, cand_id, interview_no):
    c.execute('SELECT * FROM analysis WHERE comp_ID=? AND job_title=? AND cand_ID=? AND interview_no=?',\
                (comp_id, job_title, cand_id, interview_no))
    data = c.fetchall()
    return data
