import sqlite3
conn = sqlite3.connect('database_final.db', check_same_thread=False)
conn.execute('PRAGMA foreign_keys = 3')
c = conn.cursor()


def create_tables():
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
                cand_ID             text    PRIMARY KEY,
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
                PRIMARY KEY (cand_ID, comp_ID, job_title, interview_no, question_no)
                FOREIGN KEY (cand_ID) REFERENCES candidate (cand_ID),
                FOREIGN KEY (comp_ID,job_title) REFERENCES job (comp_ID,job_title)
                )''')
    conn.commit()

def view_schema():
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return c.fetchall()

def delete_table(table_name):
    c.execute('DROP TABLE "{}"'.format(table_name))
    conn.commit()
### Company table related functions ###
def view_company_data():
    c.execute('SELECT * FROM company')
    data = c.fetchall()
    return data

def get_company_IDs():
    c.execute('SELECT comp_ID FROM company')
    data = c.fetchall()
    return data


def add_company(comp_ID, comp_name, comp_pass, website):
    c.execute('''INSERT INTO company(comp_ID, comp_name, comp_pass, website)
                 VALUES (?,?,?,?)''', (comp_ID, comp_name, comp_pass, website))
    conn.commit()

def get_company(comp_id):
    c.execute('SELECT * FROM company WHERE comp_ID="{}"'.format(comp_id))
    data = c.fetchall()
    return data
    
### Jobs table related functions ####
def view_jobs():
    c.execute('SELECT * FROM job')
    data = c.fetchall()
    return data
def add_job(job_title, job_req, job_description, comp_ID):
    c.execute('''INSERT INTO job(job_title, job_req, job_description, comp_ID)
                 VALUES (?,?,?,?)''', (job_title, job_req, job_description, comp_ID))
    conn.commit()

def get_job(job_title, comp_id):
    c.execute('SELECT * FROM job WHERE job_title=? AND comp_ID=?', (job_title, comp_id))
    data = c.fetchall()
    return data

def get_jobs_comp(comp_id):
    c.execute('SELECT * FROM job WHERE comp_ID="{}"'.format(comp_id))
    data = c.fetchall()
    return data

def update_job(job_title, comp_id, job_req, job_description):
    c.execute('UPDATE job SET job_req=?, job_description=? WHERE job_title=? AND comp_ID=?',\
                (job_req, job_description, job_title, comp_id))
    conn.commit()
    data = c.fetchall()
    return data

def delete_job(job_title, comp_id):
    c.execute('''DELETE FROM job WHERE job_title=? AND comp_ID=?''',\
        (job_title, comp_id))
    conn.commit()

### Candidate table related functions ####
def view_candidate_data():
    c.execute('SELECT * FROM candidate')
    data = c.fetchall()
    return data

def get_cand(cand_id):
    c.execute('SELECT * FROM candidate WHERE cand_id="{}"'.format(cand_id))
    data = c.fetchall()
    return data

def update_cand(candidate_id_edit, candidate_name_edit, candidate_qual_edit):
    c.execute('UPDATE candidate SET cand_name=?, cand_qualifications=? WHERE cand_ID=?',\
                (candidate_name_edit, candidate_qual_edit, candidate_id_edit))

def add_candidate(cand_ID, cand_name, cand_qualifications):
    c.execute('''INSERT INTO candidate(cand_ID, cand_name, cand_qualifications)
                 VALUES (?,?,?)''', (cand_ID, cand_name, cand_qualifications))
    conn.commit()
    
### Analysis table related functions ###
def view_analysis_data():
    c.execute('SELECT * FROM analysis')
    data = c.fetchall()
    return data

def add_analysis(cand_ID, comp_ID, job_title, interview_no, question_no, FER , FER_score, tone, tone_score, fluency, fluency_score, coherence_score, overall_score):
    c.execute('''INSERT INTO analysis(cand_ID, comp_ID, job_title, interview_no, question_no, FER , FER_score, tone, tone_score, fluency, fluency_score, coherence_score, overall_score)
                 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', (cand_ID, comp_ID, job_title, interview_no, question_no, FER , FER_score, tone, tone_score, fluency, fluency_score, coherence_score, overall_score))
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

def get_analysis_comp(comp_id):
    c.execute('SELECT * FROM analysis WHERE comp_ID="{}"'.format(comp_id))
    data = c.fetchall()
    return data

def get_analysis_with_job(comp_id, job_title):
    c.execute('SELECT * FROM analysis WHERE comp_ID=? AND job_title=?',(comp_id, job_title))
    data = c.fetchall()
    return data

def get_analysis_with_cand(comp_id, cand_id):
    c.execute('SELECT * FROM analysis WHERE comp_ID=? AND cand_ID=?',(comp_id, cand_id))
    data = c.fetchall()
    return data

def get_analysis_with_job_cand(comp_id, job_title, cand_id, interview_no):
    c.execute('SELECT * FROM analysis WHERE comp_ID=? AND job_title=? AND cand_ID=? AND interview_no=?',\
                (comp_id, job_title, cand_id, interview_no))
    data = c.fetchall()
    return data

def get_one_analysis(comp_ID, job_title, cand_ID, interview_no, question_no):
    c.execute('''SELECT * FROM analysis WHERE cand_ID=? AND comp_ID=? AND job_title=? AND 
              interview_no=? AND question_no=?''', (cand_ID, comp_ID, job_title, interview_no, question_no))
    data = c.fetchall()
    return data
    