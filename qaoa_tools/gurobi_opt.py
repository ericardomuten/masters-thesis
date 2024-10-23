import gurobipy as gp
from gurobipy import GRB

def gurobi_minimize(N, Q, binary_variables="0/1"):
    """Finding solution bitstring with Gurobi Python API.

        Given a QUBO matrix Q, find the solution bitstring that minimize:
        x.T @ Q @ x
        with x is binary variable vector.

        Parameters
        ----------
        N : int
            The number of variables in x.
        Q : 2D numpy array or 2D scipy sparse matrix.
            The QUBO matrix.
        binary_variables  : string, default="0/1"
            Choose between 2 options for x:
            - "0/1" for treating the binary variables as 0 or 1.
            - "-1/1" for treating the binary variables as -1 or 1.

        Returns
        -------
        solution_bitstring : 1D numpy array
            A 1D numpy array as the solution output of Gurobi.
        min_obj_val : float
            A value of the x.T @ Q @ x using the 'solution_bitstring' as x.
    """

    m = gp.Model("matrix1")
    m.setParam('OutputFlag', False)

    # MIPFocus: 2 is to force the model to focus more attention on proving optimality
    # Read further here https://www.gurobi.com/documentation/current/refman/mipfocus.html
    m.setParam('MIPFocus', 2)

   # generate binary variables in the amount of N (number of vertices)
    x = m.addMVar(shape=N, vtype=GRB.BINARY, name="x")

    # selecting the correct binary variables
    if binary_variables == "0/1":
        # binary variables of 0 and 1
        m.setObjective(x @ Q @ x, GRB.MINIMIZE)
        m.optimize()
        solution_bitstring = x.X
    
    elif binary_variables == "-1/1":
        # binary variables of -1 and 1
        m.setObjective((2*x - 1) @ Q @ (2*x - 1), GRB.MINIMIZE)
        m.optimize()
        solution_bitstring = 2*x.X - 1  # convert 0/1 binary to -1/1 binary
    
    min_obj_val = m.ObjVal

    return solution_bitstring, min_obj_val