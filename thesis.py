def get_range_percentages(data_frame,attribute,attr_ranges,range_unit,max_range=100):
    header = []
    data_value = []
    data_percent = []
    no_of_records = len(data_frame)
    for range_min,range_max in attr_ranges:
        rdf = data_frame[attribute][(data_frame[attribute] >= range_min) & (data_frame[attribute] <= range_max)]
        if (range_max == max_range):
            header_name = ">" + str(range_min) + " " + range_unit
        else:
            header_name = str(range_min) + "-" + str(range_max) + " "+ range_unit
        rdf_value = len(rdf) *1.0
        rdf_percentage = rdf_value*100.0/no_of_records
        header.append(header_name)
        data_value.append(rdf_value)
        data_percent.append(rdf_percentage)        
    return [header,data_value,data_percent]

def get_cat_percentages(data_frame,attribute,categories=None):
    header = []
    data_value = []
    data_percent = []
    no_of_records = len(data_frame)
    if (categories is None):
        categories = sorted(data_frame[attribute].unique())
    for category in categories:
        rdf = data_frame[attribute][data_frame[attribute] == category]
        header_name = category
        rdf_value = len(rdf) *1.0
        rdf_percentage = rdf_value*100.0/no_of_records
        header.append(header_name)
        data_value.append(rdf_value)
        data_percent.append(rdf_percentage)        
    return [header,data_value,data_percent]

def print_attr_stats(data_frame,attribute):
    st = data_frame[attribute].describe()
    print attribute + " Statistics"
    print "Number of elements:%d"%(st[0])
    print "ranges from %d to %d with mean=%.2f and SD=%.2f"%(st[3],st[7],st[1],st[2])

def plot_graph(mydf,style=None,fname=None,colormap=None,stacked=False):
    import matplotlib 
    import matplotlib.pyplot as plt
    cmap = matplotlib.cm.Accent
    if style:
	plt.style.use(style)
    if colormap:
	cmap = colormap
    mydf.plot(kind='bar',fontsize=15,figsize=(8,5),colormap=cmap,rot=360,stacked=stacked)
    if fname:
    	plt.savefig(fname)

def analyse_range(data,ranges,attribute,attr_unit,convert_zero=False):
    from pandas import DataFrame
    import numpy as np
    from scipy.stats import chi2_contingency

    def transform_zero(val):
    	if (val == 0):
    		val = 1e-10
    	return val

    (pdf_a,pdf_b) = data
    header_a,data_a_value,data_a_percent = get_range_percentages(pdf_a,attribute,ranges,attr_unit)
    header_b,data_b_value,data_b_percent = get_range_percentages(pdf_b,attribute,ranges,attr_unit)
    mydf = DataFrame(columns=header_a,data=[data_a_percent,data_b_percent],index=['Group-A','Group-B'])
    obs = np.array([data_a_value,data_b_value])
    if (convert_zero):
      vecfunc = np.vectorize(transform_zero)
      obs = vecfunc(obs)
    arr = chi2_contingency(obs,correction=False)
    chi_square_value = arr[0]
    p_value = arr[1]
    return (mydf,obs,chi_square_value,p_value)

def analyse_category(data,attribute,categories=None):
    from pandas import DataFrame
    import numpy as np
    from scipy.stats import chi2_contingency
    (sdf_a,sdf_b) = data
    header_a,data_a_value,data_a_percent = get_cat_percentages(sdf_a,attribute,categories)
    header_b,data_b_value,data_b_percent = get_cat_percentages(sdf_b,attribute,categories)
    mydf = DataFrame(columns=header_a,data=[data_a_percent,data_b_percent],index=['Group-A','Group-B'])
    obs = np.array([data_a_value,data_b_value])
    arr = chi2_contingency(obs,correction=False)
    chi_square_value = arr[0]
    p_value = arr[1]
    return (mydf,obs,chi_square_value,p_value)
