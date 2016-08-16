/*
A KBase module: mcashman_FS
*/

module mcashman_FS {
    /*
        Insert your typespec information here.
    */

	
	typedef structure{
		string workspace_name;
		string pangenome_ref;
		list <string> genomes;
		list <string> classes;
		int runCount;
	}FSParams;

	typedef structure{
		string temp;
		string report_name;
		string report_ref;
	}FSOutput;

	funcdef FeatureSelection(FSParams params) returns (FSOutput) authentication required;
	
};
