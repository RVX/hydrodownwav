"""
download_class.py

 a super class with some useful methods for downloading data from each source. This ensures standardisation between subclasses for the API and the CLI.

"""

import os

from datetime import datetime
import git




class BaseDownloadClass:
    def __init__(self, ):
        pass

    def __post_init__(self):
        self.deployments = self.get_deployments()

    def get_deployments(self,):
        """
        a list of deployments, each deployment is a day of data, containing a dict of the following:
        {
            'date': 'YYYY-MM-DD',
            'latitude': float,
            'longitude': float,
            'depth': float,
            'license': str,
            'source': str,
            # any other information that is useful to save
        }
        """
        raise NotImplementedError("Subclasses must implement this method")
    

    def download_data(self, min_lat, max_lat, min_lon, max_lon, min_depth, max_depth, license, start_time, end_time, save_dir):
        raise NotImplementedError("Derived classes must implement this method.")
    
    def filter_deployments(self, min_lat, max_lat, min_lon, max_lon, min_depth, max_depth, license, start_time, end_time):
        """
        Filter deployments based on the specified parameters
        """
    
        deployments_out = [d for d in self.deployments if d['latitude']>=min_lat and d['latitude']<=max_lat and d['longitude']>=min_lon and d['longitude']<=max_lon and d['depth']>=min_depth and d['depth']<=max_depth ]
    
        if len(deployments_out)==0:
            print("No deployments found for the specified location.")
            return deployments_out

        deployments_out = [d for d in self.deployments if d['date']>=datetime.strptime(start_time, '%Y-%m-%d') and d['date']<=datetime.strptime(end_time, '%Y-%m-%d')]

        if len(deployments_out)==0:
            print("No deployments found for the specified time range.")
            return deployments_out

        if license is not None:
            deployments_out = [d for d in deployments_out if d['license']==license]

        if len(deployments_out)==0:
            print("No deployments found for the specified license.")
            return deployments_out
        
        return deployments_out
    
    def get_git_hash(self):
        return git.Repo(search_parent_directories=True).head.object.hexsha
    
    
    def log(self, message):
        print(message)

    def read_log(self):
        with open('log.txt', 'r') as f:
            return f.read()