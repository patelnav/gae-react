# GAE-REACT #
## Project template ##
This base configuration includes:
*   Backend: [Google AppEngine Standard (python)](https://cloud.google.com/appengine/docs/python/) (abbr: GAE)
    with [Flask](http://flask.pocoo.org/) at [/default](/default)

*   Backend: React app (configured through [create-react-app](https://github.com/facebook/create-react-app)) at [/web](/web)

*   Scripts
    * [run](/run): Runs **GAE** local server, **React**'s Node server
    * [test](/test): Runs pytest and yarn test
        * Installs pytest+deps and runs [_dependencies](/_dependencies)
    * [venv](/venv): Generates virtualenv for the project
        * **All commands** will cause venv ensure an environment has been created
        * `source venv`: Will load it into your current shell
        * `venv -p`: Will return the path of the virutal environment
    * [_dependencies](/_dependencies): Makes sure GAE and React dependencies are installed
    * [_clean](/_clean): Cleans all temp files created by run, test & venv
        * Also deletes all .pyc files in project