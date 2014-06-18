r = {
'Address': "36th St. at Walnut St., Philadelphia , Pennsylvania, 19104",
'GoogleLink': "http://maps.google.com/?q=39.9531474%2C%20-75.1947825%20(%22University+Square+Farmers'+Market%22)",
'Products': "Baked goods; Eggs; Fresh fruit and vegetables; Honey; Canned or preserved fruits, vegetables, jams, jellies, preserves, salsas, pickles, dried fruit, etc.; Maple syrup and/or maple products; Meat; Poultry; Prepared foods (for immediate consumption)",
'Schedule': "06/04/2014 to 11/05/2014 Wed: 10:00 AM-3:00 PM;<br> <br> <br> "
}

l = [
{
'id': "1001393",
'marketname': "19.1 Ada Farmer's Market"
},
{
'id': "1001358",
'marketname': "42.4 Durant Farmers Market"
},
{
'id': "1005968",
'marketname': "50.4 Market Place On Broadway"
},
{
'id': "1002005",
'marketname': "57.5 Shawnee Farmers Market"
},
{
'id': "1005145",
'marketname': "57.5 Pottawatomie County Farmers CO-OP Market"
},
{
'id': "1009439",
'marketname': "59.1 Farmers Market in Denison "
},
{
'id': "1000841",
'marketname': "59.2 Downtown Denison Farmers Market"
},
{
'id': "1006382",
'marketname': "65.8 Hugo Farmers Market"
},
{
'id': "1004062",
'marketname': "66.2 Wilburton Farmers Market"
},
{
'id': "1006618",
'marketname': "66.6 Eufaula Farmer's Market"
},
{
'id': "1005695",
'marketname': "72.4 Norman Farmers Market"
},
{
'id': "1001670",
'marketname': "78.1 Eastern Oklahoma County Farmers Market"
},
{
'id': "1005628",
'marketname': "78.5 Talihina Farmers' Market"
},
{
'id': "1001851",
'marketname': "79.6 Blanchard Farmers' Market"
},
{
'id': "1005046",
'marketname': "80.9 Newcastle Downtown Farmers Market"
},
{
'id': "1008834",
'marketname': "81.8 Market Square, Farmers Market"
},
{
'id': "1006297",
'marketname': "84.6 Valliant Farmers Market"
},
{
'id': "1002410",
'marketname': "85.6 National Women In Ag Assoc. Community Farmers Market"
},
{
'id': "1007048",
'marketname': "85.8 OSDH Wellness Farmers' Market"
}
]

def get_result(results):
    if type(results) == type({}):
        # if dict begin creating objects
        return results
    else:
        # check again
        for result in results:
            return get_results(result)


print get_result(l)










'''
a = {'jay': 36, 'penney': 0, 'mom': 59}
b = {'level2': {'dad': 1, 'dad2':2}, 'level': {'dad': 1, 'dad2':2}, 'level2': {'dad': 1, 'dad2':2},}
c = {'jay': 3, 'penney': 3, 'mom': 3}
#x = {a, b, c}

def check_dict(var):
    
    i=0
    
    if type(var) == type({}):
        try:
            for k,v in vars.items():
                i += check(v)
                return i
        except:
            i+=1
            return i
    else:
        return i

count = check_dict(b)
print 'count = ', count
'''

