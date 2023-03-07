crab_job_status: skim_version_year = 2018
crab_job_status: grep =.
crab_job_status:
	cd crab_projects/ ;\
        for fn in `ls *${skim_version_year}* -d | grep ${grep} ` ;\
        do \
        echo $$fn ;\
        crab status -d $$fn ;\
        done
