import random
import numpy as np
import time

def inference(epsilon, N):
    
    #tempoiniziale=time.time()
    
    c_out=6./(1./epsilon + 1)
    c_in=6./(epsilon + 1)
    
    #Metto i punti nelle loro famiglie (n_a=n_b=0.5)
    
    t=np.zeros(N)
    
    for i in range(N):
        if(random.randint(0,1)==0):
            t[i]=1
            
    #Creo la matrice di adiacenza
    
    coppie=[]   #coppie è una lista che contiene tutte le coppie collegate
    maxi=0   #maxi è il grado massimo al variare dei nodi
    
    for i in range(N):
        ci=0
        for j in range(i):
            if(t[i]==t[j]):
                if(random.randint(1,10*N)<=10*c_in):
                    coppie.append([i,j])
                    coppie.append([j,i])
                    ci+=1
            else:
                if(random.randint(1,10*N)<=10*c_out):
                    coppie.append([i,j])
                    coppie.append([j,i])
                    ci+=1
        if(ci>maxi):
            maxi=ci
    
    
    #adiacenza mette nella riga i-esima tutte le j collegate con i. Nello spazio restante mette -1.
    
    adiacenza = [[-1 for x in range(maxi)] for y in range(N)] 
    
    #   Per ogni coppia in "coppie", prendo il primo dei due nodi. Nella corrispondente
    #   riga in "adiacenza" aggiungo l'indice del secondo nodo.
    
    for i in range(len(coppie)):
        for k in range(maxi):
            if(adiacenza[coppie[i][0]][k]==-1):
                adiacenza[coppie[i][0]][k]=coppie[i][1]
                break
    
                
    #Inizializzo psij, psi, h. psij[i][k] contiene il vettore psi_{ij} con j=adiacenza[i][k].
                    
    psij=np.zeros((N,maxi,2))
    psi=np.zeros((N,2))
    
    for i in range(N):
        for j in range(maxi):
            psij[i][j][0]=random.uniform(0,1)
            psij[i][j][1]=1-psij[i][j][0]
            
            #psij[i][j][0]=1-t[i]   #Se voglio dargli una mano all'inizio
            #psij[i][j][1]=t[i]
            
            
    for i in range(N):
        psi[i][0]=random.uniform(0,1)
        psi[i][1]=1-psi[i][0]
        
        #psi[i][0]=1-t[i]   #Se voglio dargli una mano all'inizio
        #psi[i][1]=t[i]
    
    h=np.zeros(2)
    
    for q in range (2):
        for k in range (N):
            h[q]+=(c_in*psi[k][q]+c_out*psi[k][1-q])
        h[q]=h[q]/N
    
    
    #Ora posso creare delle psi più sensate. Non so se è necessario questo step.
    
    def calcolaproduttazzo(i):
        
        #Voglio la produttoria in equazione (28)
        
        produttazzo=np.array([1.,1.])
        
        for j in adiacenza[i]:
            for q in range(2):
                for k in range(maxi):
                    if(adiacenza[j][k]==i):
                        
                        #psij[j][k] è semplicemente psi_{ji}
                        
                        produttazzo[q]*=(c_in*psij[j][k][q]+c_out*psij[j][k][1-q])
                        
        return produttazzo
    
    
    for i in range(N):
        
        produttazzo=calcolaproduttazzo(i)
        
        for q in range(2):
            psi[i][q]=np.exp(-h[q])*produttazzo[q]
            
        temp=psi[i][0]/(psi[i][0]+psi[i][1])
        psi[i][1]=psi[i][1]/(psi[i][0]+psi[i][1])
        psi[i][0]=temp
    
    #Parametri di uscita dal ciclo
    
    criterio=0.01*N
    tmax=500
    conv=criterio+1
    
    tt=0   #Numero di iterazioni
    new=np.zeros(2)
    prodotto=np.zeros(2)
    
    #Ciclo di aggiornamenti
    
    while(conv>criterio and tt<tmax):
        conv=0
        tt=tt+1
        tempo0=time.time()
        
        I=np.arange(N)
        random.shuffle(I)   #Aggiorno con ordine random
        
        for i in I:
            
            produttazzo=calcolaproduttazzo(i)
            
            disordinato=[]   #Vettore che contiene tutti i vicini di i in ordine sparso.
            for k in range(maxi):
                if(adiacenza[i][k]!=-1):
                    disordinato.append(adiacenza[i][k])
            random.shuffle(disordinato)
            
            for j in disordinato:
                
                
                #Utilizzo la formula (26). "Prodotto" è la produttoria in questa formula.
                
                for q in range(2):
                    for k in range(maxi):
                        if(adiacenza[j][k]==i):
                            prodotto[q]=produttazzo[q]/(c_in*psij[j][k][q] + c_out*psij[j][k][1-q])
                            new[q]=np.exp(-h[q])*prodotto[q]
            
                temp=new[0]/(new[0]+new[1])
                new[1]=new[1]/(new[0]+new[1])
                new[0]=temp
                
                
                #Guardo la variazione causata dall'aggiornamento
                
                for k in range(maxi):
                    if(adiacenza[i][k]==j):
                        conv+=abs(new[0]-psij[i][k][0])+abs(new[1]-psij[i][k][1])
                        break
        
                
                #Aggiorno psi[j] grazie al nuovo psi_{ij}
                
                vecchiepsi=[psi[j][0],psi[j][1]]
                
                for q in range(2):
                    psi[j][q]*=(c_in*new[q]+c_out*new[1-q])/(c_in*psij[i][k][q]+c_out*psij[i][k][1-q])
                
                temp=psi[j][0]/(psi[j][0]+psi[j][1])
                psi[j][1]=psi[j][1]/(psi[j][0]+psi[j][1])
                psi[j][0]=temp
                
                
                #Stesso discorso per il campo medio.
                
                for q in range (2):
                    h[q]+=((c_in*psi[j][q]+c_out*psi[j][1-q])-(c_in*vecchiepsi[q]+c_out*vecchiepsi[1-q]))/N
            
                psij[i][k][0]=new[0]
                psij[i][k][1]=new[1]
               
                
        deltat=time.time()-tempo0
        #strdeltat=str(int(deltat))+'.'+str(int(100*deltat)%100)
        
        #print('Convergenza =', int(100 * conv / N))
        #print('Tempo iterazione =', strdeltat)
        #print('Iterazione =', tt, '\n')
    
    guess=0.0
    
    for i in range(N):
        if((psi[i][0]>=0.5 and t[i]==0) or (psi[i][1]>0.5 and t[i]==1)):
            guess+=1
    
    guess=max(N-guess,guess)   #Quanti ne ho azzeccati
    
    Overlap=(guess/N-0.5)*2
    #Deltat=time.time()-tempoiniziale
    #strOverlap=str(int(Overlap))+'.'+str(int(100*Overlap)%100)
    
    #print("\n")
    #print(Overlap)
    #print('Tempo totale =', str(int(Deltat))+'.'+str(int(100*Deltat)%100))
    
    return(tt, deltat, Overlap, psi, t)
    
#------------------------------------------------------------------------------

Ns=[5000]
epsilons=np.linspace(0.22, 0.30, 41)


with open('Dati5000_x.txt', 'w') as f:
    f.write('N\t'+'epsilon\t'+'iterazioni\t'+'tempoiterazione\t'+'Overlap')
    for N in Ns:
        for epsilon in epsilons:
            
            print(N," ",epsilon)
            
            output=inference(epsilon,N)
            
            riga=[N, epsilon]
            for i in range(3):
                riga.append(output[i])
            
            f.write('\n')
            for item in riga:
                f.write("%s\t" % item)
















