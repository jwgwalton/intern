# This script is to set up the local dev environment

conda_env_name="intern-dev-env"
jupyter_kernel_name="intern-dev-env"

conda create --name ${conda_env_name} python=3.9.15 --yes
# note we need to import the conda script otherwise current shell isn't ready for anaconda...
source /anaconda/bin/activate && conda activate ${conda_env_name}

pip install -r requirements.txt

pip install jupyter
python -m ipykernel install --user --name ${conda_env_name} --display-name "${jupyter_kernel_name}"

echo
echo
echo "Environment build complete."
echo
echo "Enter 'conda activate ${conda_env_name}' at command line to locally activate the environment."
echo
echo "To use in Jupyter, please select kernel '${jupyter_kernel_name}'."
echo "Note: you may have to restart Jupyter for it to detect the new kernel."
echo
echo "To remove:"
echo "conda env remove --name ${conda_env_name}"
echo "jupyter kernelspec uninstall ${conda_env_name}"
echo
