from fabric.api import sudo, cd, run, env, local, prefix

env.hosts = ['ocukphotocomp.growse.com']
env.use_ssh_config = True


def deploy():
    local('git rebase master deploy')
    local('git push')
    local('git checkout master')
    with cd('/home/growse/django-sites/ocukphotocomp.growse.com'):
        with prefix('source bin/activate'):
            run('git pull')
            run('pip install --upgrade -r requirements.txt')
            run('./manage.py migrate photocomp')
            run('./manage.py collectstatic --noinput')
            sudo('touch /etc/uwsgi/apps-enabled/ocukphotocomp.growse.com.ini')
