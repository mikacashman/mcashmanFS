/*
A KBase module: mcashman_FS
*/

module mcashman_FS {
    /*
        Insert your typespec information here.
    */

	
	typedef structure{
		string workspace_name;
		list <int> classes;
		string pangenome_ref;
	}FSParams;

	typedef structure{
		string temp;
		string report_name;
		string report_ref;
	}FSOutput;

	funcdef FeatureSelection(FSParams params) returns (FSOutput) authentication required;
	
};
