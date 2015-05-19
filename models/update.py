#!/usr/bin/python

import subprocess
from flask.ext import restful

class Update(restful.Resource):
    def get(self):
        commits = self.git_list_commits()
        return {
            'current_version': self.git_version(),
            'commits': commits,
            'commits_behind': len(commits)
        }

    def git_list_commits(self):
        commits = subprocess.check_output(['git', 'log','--oneline','HEAD..origin']).strip('\n').split('\n')
        print commits
        return commits

    def git_version(self):
        #git rev-parse HEAD
        return subprocess.check_output(['git','rev-parse','HEAD']).strip()

    def git_fetch(self):
        #git log --oneline HEAD..origin | wc -l
        return subprocess.check_output(['git','fetch','--all']).strip()

    def git_pull(self):
        return subprocess.check_output(['git','pull']).strip()
