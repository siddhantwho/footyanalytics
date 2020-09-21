import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.lines as mlines

def plot_actions(actions_df, team, value = 'offence_value'):
    
    plt.figure(figsize = (6,9),dpi = 300)
    o_rate = list(actions_df[value])

    maxo = max(o_rate)
    mino = min(o_rate)

    for index, row in actions_df.reset_index().iterrows():

        actno = '(' + str(index +1) + ')'
        jersey = str(int(row.jersey_number))
        #annot = actno + ' - ' + '(' + jersey +')'
        #annot = actno
        
        cmobj = matplotlib.cm.ScalarMappable(norm = None,cmap = 'YlOrRd')
        cmap = cmobj.get_cmap()
        ovalue = (row[value] - mino)/(maxo - mino)
        colour = cmap(ovalue)

        if (row.team == team):
            #colour = 'red'
            pressure = '<'
        else:
            colour = 'blue'
            pressure = '>'

        xi = (row.start_x)*20
        yi = (row.start_y)*20
        xf = (row.end_x)*20
        yf = (row.end_y)*20
        dx = xf - xi
        dy = yf - yi

        ax = xi
        #ay = (yi+500 if yi <800 else yi-50)
        ay = yi - 500

        if (row.action == 'Pass') or (row.action == 'Clearance'):
            plt.plot([xi,xf],[yi,yf],color=colour,ls = '--')

            plt.annotate(annot,(xi,yi),(ax,ay),color=colour,size=6)
            plt.arrow((xi+xf)/2,(yi+yf)/2,dx/(dx**2 + dy**2),dy/(dx**2 + dy**2),color='white',width = 0, head_width = 25,
                      ls = '-', length_includes_head = True)

        if (row.action == 'Ball Receipt*'):
            plt.plot(xi,yi,color=colour, marker = '.')

        if (row.action == 'Carry') or (row.action == 'Dribble'):
            plt.plot([xi,xf],[yi,yf],color=colour, ls = ':')

            plt.annotate(annot,(xi,yi),(ax,ay),color=colour,size=6)

        if (row.action == 'Pressure') or (row.action == 'Duel'):
            plt.plot(xi,yi, color= colour, marker= pressure) 

        if (row.action == 'Shot'):
            plt.arrow(xi,yi,dx,dy,color=colour,width = 10, head_width = 40,ls = '-',
                     length_includes_head = True)

        if (row.action == 'Interception') or (row.action == 'Block') or (row.action == 'Dispossessed') or ((row.action == 'Goalkeeper') and (row.result != 'No Touch')):
            plt.plot(xi,yi, color= colour, marker= 'x',markersize= 6)

            
    pass_ = mlines.Line2D([], [], color='red', ls='--', linestyle='None',
                          markersize=6, label='Pass')
    carry_ = mlines.Line2D([], [], color='red', ls=':', linestyle='None',
                          markersize=6, label='Carry')
    shot_ = mlines.Line2D([], [], color='red', ls='-', linestyle='None',
                          markersize=6, label='Shot')
    block_ = mlines.Line2D([], [], color='red', marker ='x', linestyle='None',
                          markersize=6, label='Block')
    

    plt.legend(handles=[carry_, pass_,shot_,block_],loc=9,fontsize =6.5)
    
    img = plt.imshow(np.array([[0,100]]), cmap="YlOrRd")
    img.set_visible(False)

    plt.colorbar(orientation="vertical",shrink = 0.35,ticks = [0,25,50,75,100])

    plt.axis('off')
    plt.imshow(pitch)
    plt.show()
