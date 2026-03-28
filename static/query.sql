SELECT ja.id,
       ja.company_name,
       ja.role,
       ja.job_type,
       ja.status,
       ja.applied_date,
       ja.salary,
       ja.location,
       ja.source,
       ja.contact_person,
       ja.notes,
       ja.created_at,
       ja.user_id
FROM job_application ja
         INNER JOIN users
                    ON ja.user_id = users.id