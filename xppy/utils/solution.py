'''
Created on Feb 11, 2010

@author: enxjn
'''
import numpy as np #@UnresolvedImport

####
# Reading XPPAut Auto output files (.p and .q)
####
class Solution:
    def __init__(self):
        self.ctrl = None
        self.sol  = None
        self.drv  = None
        self.p1   = None
        self.p2   = None

def parse_sl(file_name):
    '''
    Function parses XPPAut generated solution file (one with extension 'q')
    named file_name and returns the solutions.
    '''
    print 'Warning! Function is obsolete, use parseSolution instead!'
    parseSolution(file_name)
    
def parseSolution(file_name):
    '''
    Function parses XPPAut generated solution file (one with extension 'q')
    named file_name and returns the solutions.
    '''
    f = open(file_name, 'r')

    i = -1
    sols = []
    for l in f:
        ll = l.split()

        # If it's user RG or LP, start to colect data
        if len(ll) == 13 and (int(ll[2]) == 4 or int(ll[2]) == 5):
            s = Solution()
            s.ctrl = np.array(ll, np.int)
            s.sol = np.ones((s.ctrl[6],s.ctrl[7]))*np.NaN
            s.drv = np.ones((s.ctrl[6],s.ctrl[7]-1))*np.NaN
            i = 0
            
            # We're loading data now
            if i >= 0:
                # Writting solution
                if i < s.ctrl[6]:
                    s.sol[i,:] = np.array(ll, np.float)
                # Skipping a line
                elif i == s.ctrl[6]:
                    i += 1
                    continue
                # Writting derivatives (?)
                elif i < 2*s.ctrl[6] + 1:
                    ii = i - s.ctrl[6] - 1;
                    s.drv[ii,:] = np.array(ll, np.float)
                elif i == 2*s.ctrl[6] + 1:
                    s.p1 = float(ll[0])
                    s.p2 = float(ll[1])
                # Incrementing counter
                i += 1
                # Checking if we're at the end of the block
                if i >= s.ctrl[8]:
                    i = -1
                    sols.append(s)
                else:
                    continue

    f.close()

    return sols

def parse_bf(file_name):
    '''
    Function parses XPPAut generated solution file (one with extension 'q')
    named file_name and returns the solutions.
    '''
    print 'Warning! Function is obsolete, use parseBifDiag instead!'
    parseBifDiag(file_name)

def parseBifDiag(file_name):
    '''
    Function parses XPPAut generated bif. diagram file (one with extension 'p')
    named file_name and returns the data.
    '''
    print 'Parsing bifurcation diagram file:',file_name
    f = open(file_name, 'r')
    d = []
    for l in f:
        ll = l.split()
        if ll[0] != '0':
            # Fix for merging '-' sign for lond point number
            if ll[0].rfind('-') > 0:
                ll_rest = ll[1:]
                ll = ll[0].rsplit('-',1)
                ll[1] = '-'+ll[1]
                ll.extend(ll_rest)
            # If it's 'normal' branch, append period column 
            if int(ll[0]) > 0:
                ll.append('0')
            d.append(ll)
    f.close()
    return np.array(d, np.float)
