vector cls_p[];
int cls_n[];
int cls_i[];

for (int i=0; i<@Npts; i++) 
{
	if (inpointgroup(0,"inCluster", i))
    {
 		// get cluster membership
		int cluster = point(0, "clsID", i);
		vector pos = point(0, "P", i);
 		int index = point(0, "ptnum", i);

		// add position to correct array bucket
		cls_p[cluster] += pos;
		cls_n[cluster] += 1;
		push(cls_i, index);
    }

    else
    {
		setpointattrib(geoself(), "center", i, 0, "set");    	
    }
}
 
foreach (int i; int item; cls_n) //enumerate array
{
	cls_p[i] /= item;
}

foreach (int item; cls_i)
{
	int cluster = point(0, "clsID", item);
	setpointattrib(geoself(), "center", item, cls_p[cluster], "set");
}
