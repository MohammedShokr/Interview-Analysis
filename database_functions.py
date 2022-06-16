import sqlite3
conn = sqlite3.connect('database_final.db', check_same_thread=False)   # connect to database
conn.execute('PRAGMA foreign_keys = 3')  
c = conn.cursor()


def create_tables():
    # create the tables og the database
    # To be run only once
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
    # view the database schema, all the tables
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return c.fetchall()

def delete_table(table_name):
    # delete the table with its name
    c.execute('DROP TABLE "{}"'.format(table_name))
    conn.commit()
    
###################### Company table related functions #####################
def view_company_data():
    # get all the companies table, for the system manager use only
    c.execute('SELECT * FROM company')
    data = c.fetchall()
    return data

def get_company_IDs():
    # gets all the available ids of the companies in the system
    c.execute('SELECT comp_ID FROM company')
    data = c.fetchall()
    return data


def add_company(comp_ID, comp_name, comp_pass, website):
    # add a new company with the needed given information, used in signup page
    c.execute('''INSERT INTO company(comp_ID, comp_name, comp_pass, website)
                 VALUES (?,?,?,?)''', (comp_ID, comp_name, comp_pass, website))
    conn.commit()

def get_company(comp_id):
    # To retrieve the information of a certain company with its ID
    c.execute('SELECT * FROM company WHERE comp_ID="{}"'.format(comp_id))
    data = c.fetchall()
    return data
    
############################ Jobs table related functions ##############################
def view_jobs():
    # get the full table of all jobs of all companies in the system
    c.execute('SELECT * FROM job')
    data = c.fetchall()
    return data

def add_job(job_title, job_req, job_description, comp_ID):
    # add a new job to the table with the gien details
    c.execute('''INSERT INTO job(job_title, job_req, job_description, comp_ID)
                 VALUES (?,?,?,?)''', (job_title, job_req, job_description, comp_ID))
    conn.commit()

def get_job(job_title, comp_id):
    # get the details of a certain job of a certain company
    c.execute('SELECT * FROM job WHERE job_title=? AND comp_ID=?', (job_title, comp_id))
    data = c.fetchall()
    return data

def get_jobs_comp(comp_id):
    # get the full jobs details of a certain company
    c.execute('SELECT * FROM job WHERE comp_ID="{}"'.format(comp_id))
    data = c.fetchall()
    return data

def update_job(job_title, comp_id, job_req, job_description):
    # update a certain job's details
    c.execute('UPDATE job SET job_req=?, job_description=? WHERE job_title=? AND comp_ID=?',\
                (job_req, job_description, job_title, comp_id))
    conn.commit()
    data = c.fetchall()
    return data

def delete_job(job_title, comp_id):
    # delete a certain job
    delete_analysis_job(comp_id, job_title)
    c.execute('''DELETE FROM job WHERE job_title=? AND comp_ID=?''',\
        (job_title, comp_id))
    conn.commit()

############################# Candidate table related functions #############################
def view_candidate_data():
    # gets the full table of the candidate details in the system
    c.execute('SELECT * FROM candidate')
    data = c.fetchall()
    return data

def get_cand(cand_id):
    # retrieve the details of a certain candidate
    c.execute('SELECT * FROM candidate WHERE cand_id="{}"'.format(cand_id))
    data = c.fetchall()
    return data

def update_cand(candidate_id_edit, candidate_name_edit, candidate_qual_edit):
    # edit the details of a certain candidate
    c.execute('UPDATE candidate SET cand_name=?, cand_qualifications=? WHERE cand_ID=?',\
                (candidate_name_edit, candidate_qual_edit, candidate_id_edit))
    conn.commit()
    data = c.fetchall()
    return data

def add_candidate(cand_ID, cand_name, cand_qualifications):
    # add a new candidate with the inputed details
    c.execute('''INSERT INTO candidate(cand_ID, cand_name, cand_qualifications)
                 VALUES (?,?,?)''', (cand_ID, cand_name, cand_qualifications))
    conn.commit()
    
############################## Analysis table related functions ##############################
def view_analysis_data():
    # get the full table of all analysis results, for debugging and system manager use only
    c.execute('SELECT * FROM analysis')
    data = c.fetchall()
    return data

def add_analysis(cand_ID, comp_ID, job_title, interview_no, question_no, FER , FER_score, tone, tone_score, fluency, fluency_score, coherence_score, overall_score):
    # add a new analysis result, this can be only used automatically after running the prediction models
    c.execute('''INSERT INTO analysis(cand_ID, comp_ID, job_title, interview_no, question_no, FER , FER_score, tone, tone_score, fluency, fluency_score, coherence_score, overall_score)
                 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''', (cand_ID, comp_ID, job_title, interview_no, question_no, FER , FER_score, tone, tone_score, fluency, fluency_score, coherence_score, overall_score))
    conn.commit()

def delete_one_analysis(comp_ID, job_title, cand_ID, interview_no, question_no):
    # delete a certain analysis result of a certain question in one interview of a candidate in certain job open by a certain company
    c.execute('''DELETE FROM analysis WHERE cand_ID=? AND comp_ID=? AND job_title=? AND 
              interview_no=? AND question_no=?''', (cand_ID, comp_ID, job_title, interview_no, question_no))
    conn.commit()
    
def delete_analysis_cand(cand_ID, comp_id):
    # delete all analysis data linked to a certain candidate
    c.execute('''DELETE FROM analysis WHERE cand_ID=? AND comp_ID=? ''', (cand_ID, comp_id))
    conn.commit()
    
def delete_analysis_job(comp_ID, job_title):
    # delete all analysis data of a certain job
    c.execute('''DELETE FROM analysis WHERE comp_ID=? AND job_title=?''', (comp_ID, job_title))
    conn.commit()
    
def delete_analysis_cand_job(cand_ID, comp_ID, job_title):
    # deletes all analysis results of a candidate in a certain job he applied for
    c.execute('''DELETE FROM analysis WHERE cand_ID=? AND comp_ID=? AND job_title=?
              ''', (cand_ID, comp_ID, job_title))
    conn.commit()

def get_analysis_comp(comp_id):
    # get all the analysis results table of a certain company, only used to be downloaded upon the company's request
    c.execute('SELECT * FROM analysis WHERE comp_ID="{}"'.format(comp_id))
    data = c.fetchall()
    return data

def get_analysis_with_job(comp_id, job_title):
    # get all analysis result details of a certain job
    c.execute('SELECT * FROM analysis WHERE comp_ID=? AND job_title=?',(comp_id, job_title))
    data = c.fetchall()
    return data

def get_analysis_with_cand(comp_id, cand_id):
    # get all analysis results details of a certain candidate
    c.execute('SELECT * FROM analysis WHERE comp_ID=? AND cand_ID=?',(comp_id, cand_id))
    data = c.fetchall()
    return data

def get_analysis_with_job_cand(comp_id, job_title, cand_id, interview_no):
    # get all analysis results details of a certain candidate in acertain job he applied for
    c.execute('SELECT * FROM analysis WHERE comp_ID=? AND job_title=? AND cand_ID=? AND interview_no=?',\
                (comp_id, job_title, cand_id, interview_no))
    data = c.fetchall()
    return data

def get_one_analysis(comp_ID, job_title, cand_ID, interview_no, question_no):
    # gets all the details of a certain one analysis result details
    c.execute('''SELECT * FROM analysis WHERE comp_ID=? AND job_title=? AND cand_ID=? AND 
              interview_no=? AND question_no=?''', (comp_ID, job_title, cand_ID, interview_no, question_no))
    data = c.fetchall()
    return data

def update_one_analysis(comp_ID, job_title, cand_ID, interview_no, question_no, overall_score):
    # updates all the details of a certain one analysis result details
    c.execute('UPDATE analysis SET overall_score=? WHERE comp_ID=? AND job_title=? AND cand_ID=? AND interview_no=? AND question_no=?',\
                (overall_score, comp_ID, job_title, cand_ID, interview_no, question_no))
    conn.commit()
    data = c.fetchall()
    return data

#print(get_one_analysis('5', 'Area Sales Manager', '1', 1, 1))
#delete_one_analysis('1', '5', 'Area Sales Manager', 1, 1)