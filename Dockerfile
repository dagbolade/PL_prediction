# Using a python file
FROM python:3.10-slim

# Se the working directory
WORKDIR /usr/src/app/epl

# Copy the contents of the current directory from the host into the container
# This includes the epl directory and the requirements.txt file if they are in the root directory
COPY epl/ .

# Copy the requirements.txt file from the context directory to the current WORKDIR
COPY requirements.txt .

# Install any needed packages
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install jupyter

# Make port 8888 available to the container
EXPOSE 8888

# Define envirnoment variable
ENV NAME World

# Run epl.py  when the container launches
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]

