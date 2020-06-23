# Grid Shape Configurations

def get(shape_num, a, b, state):
    '''
    Returns a preset shape.
    '''
    if shape_num == 1:
        shape = [[0,1,0],
                 [0,0,1],
                 [1,1,1]]

    elif shape_num == 2:
        shape = [[0,1,0],
                 [1,1,1],
                 [1,0,1],
                 [0,1,0]]

    elif shape_num == 3:
        k = [1,0,1,0,1]
        j = [1,0,0,0,1]
        shape = [k,j,j,j,k] 

    elif shape_num == 4:
        shape = [[0,1,1,0,1,1,0],
                 [0,1,1,0,1,1,0],
                 [0,0,1,0,1,0,0],
                 [1,0,1,0,1,0,1],
                 [1,0,1,0,1,0,1],
                 [1,1,0,0,0,1,1]]
    
    elif shape_num == 6:
        shape = [[0 for Shape in range(15)] for Shape in range(38)]
        to_be_birthed = [[23, 24, 34, 35], 
                         [0, 1, 9, 10, 22, 23],
                         [0, 1, 8, 10],
                         [8, 9, 16, 17],
                         [16, 18],  
                         [16],
                         [35, 36],
                         [35, 37],
                         [35],
                         [],  
                         [],
                         [24, 25, 26],
                         [24],
                         [25]]
        
        for b in range(len(to_be_birthed)):
            for d in to_be_birthed[b]:
                shape[d][b] = 1

    elif shape_num == 7: shape = [[1], [1], [1], [1], [1], [1], [1], [1], [1], [1]]

    elif shape_num == 8: shape = [[0,1,0], [1,1,1], [1,0,0]]

    else: shape = [[0]]

    return (shape, min(a, state.width + 2 * state.cushion - len(shape)),
            min(b, state.height + 2 * state.cushion - len(shape[0])))