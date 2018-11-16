[![Python 2.7](https://img.shields.io/badge/python-2.7.15-blue.svg)](https://www.python.org/downloads/release/python-270/)
<a href="https://codeclimate.com/github/inarli/github-jira-issue-updater/maintainability"><img src="https://api.codeclimate.com/v1/badges/fd1ed433dc911e48178f/maintainability" /></a>

# What? 
This application helps to move the issues on kanban board automatically according to Github pull request activities for the projects which are using Jira to tracking issues. 

# Why?
In our company, we are using Jira to tracking the issues and using Github to manage the sources. We have already integrated Jira with Github with a plugin and we are using a strategy for this integration for branches and commit messages. But, this plugin does not solve all the needs. For example, the issues don't move automatically when somebody creates a pull request for the issues. The issue should be in a specific board column (for example code review) after somebody creates a pull request for the issue. Before this library, we had been doing this actions by ourself, manually. Because, in QA testing side, they don't know Github and source code and code review process. They are using Jira and automatically deployed test environments. And they don't know the real staus of issue if somebody forgot the move the issue on the kanban board.

# How works?
Basically, we are using Jira API and Github Hooks mechanism to track the issues and pull request actions.

# What do you need?

1 - A Jira Account to get [api token](https://id.atlassian.com/manage/api-tokens)
2 - Permission to add a hook the repository (on Github only for now).
3 - And a Heroku account (optional)

# How can you use?

*Step 1:* You should know the transition id's of your project flow. So, you should now the next column id of the board after code review finished. Also, there is another id which is using to understand the next state of the issue on the board when the code needs some changes after code review. To learn these ids, we are using 
[this api](https://docs.atlassian.com/software/jira/docs/api/REST/7.6.1/#api/2/issue-getTransitions) endpoint.

*Step 2:* We suggest the Heroku (free one is enough) but you can use other services. You need to deploy the application. You can use Gunicorn to run as a service. Please check the Procfile for more information.

*Step 3:* After that, you need to create a webhook on github. Follow the below screenshots:
![image](https://user-images.githubusercontent.com/1387333/48555337-f762a680-e8f1-11e8-84bd-02b40c6c3a5c.png)
![image](https://user-images.githubusercontent.com/1387333/48555386-1a8d5600-e8f2-11e8-9e90-be53839a16ba.png)
![image](https://user-images.githubusercontent.com/1387333/48555248-aeaaed80-e8f1-11e8-9b13-c808b0fd033c.png)

*Step 4:* We have a .env file and we are using Postgresql to track the relation between Jira and Github. Please copy 
the `.env.dist` file as `.env` and fill the parameters. 

*Stem 5:* At the end, you need to import `sql/dump.sql` file to your database. 

Now, you are ready.

# Some Critical Points

 - Your branch names should be same with your Jira issue id. (For example, you have an issue on Jira as JIRA-1234. You 
should create a branch directly named as JIRA-1234.)

# Thanks 

@suhaboncukcu

# Need Help

You can create an issue if you need any help about the installation part.