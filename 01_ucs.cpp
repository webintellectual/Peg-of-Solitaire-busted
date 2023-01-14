#include<iostream>
#include<vector>
#include<utility>
#include<queue>
#include<unordered_set>
#include<unordered_map>
using namespace std;

struct Node{
    vector<vector<int> > state; // identity of a node
    struct Node* parent; // parent size = 0 => No parent
    // the action that was applied to the parent’s state to generate this node:
    pair<pair<int,int>, pair<int,int> > action; // first pair is the location of marble chosen
                                                // second pair is the location of empty dent chosen
    int pathCost;
    Node(){
        vector<vector<int> > st( 7, vector<int> ( 7,2) );
        for(int i=0; i<7; i++){
            for(int j=0; j<7; j++){
                if(i==0 || i==1 || i==5 || i==6){
                    if(j==2 || j==3 || j==4){
                        st[i][j]=1;
                    }
                }
                else{
                    st[i][j]=1;
                }
            }
        }
        st[3][3]=0;
        state = st;
        parent = NULL;
        pathCost =0;
    }
    Node(vector<vector<int> > st, Node* prt, int pCost){
        state = st;
        parent = prt;
        pathCost = pCost;
    }
};

struct compareCost {
	bool operator()(Node* const& n1, Node* const& n2)
	{
		// return "true" if "n1" is ordered
		// before "n2", for example:
		return n1->pathCost > n2->pathCost; // min heap
	}
};

vector<vector<int> > mirrorImg(vector<vector<int> > state){
    for(int i=0; i<7; i++){
        reverse(state[i].begin(),state[i].end());
    }
    return state;
}

vector<vector<int> > transpose(vector<vector<int> > state){
    vector<vector<int> > ans(7, vector<int> (7,2));
    for(int i=0; i<7; i++){
        for(int j=0; j<7; j++){
            ans[j][i] = state[i][j];
        }
    }
    return ans;
}

vector<vector<vector<int> > > equivalents(vector<vector<int> > state){
    vector<vector<vector<int> > > ans;
    vector<vector<int> > v1 = mirrorImg(state); // mirror image
    ans.push_back(v1);
    vector<vector<int> > v2 = state; // reversed
    reverse(v2.begin(),v2.end());
    ans.push_back(v2);

    vector<vector<int> > v3 = v1;
    reverse(v3.begin(),v3.end());
    ans.push_back(v3);

    vector<vector<int> > v4 = transpose(state);
    ans.push_back(v4);
    vector<vector<int> > v5 = mirrorImg(v4);
    ans.push_back(v5);
    vector<vector<int> > v6 = v4;
    reverse(v6.begin(),v6.end());
    ans.push_back(v6);
    vector<vector<int> > v7 = mirrorImg(v6);
    ans.push_back(v7);

    return ans;
}

vector<vector<int> > goal(7, vector<int> ( 7,2));
void setGoal(){
    vector<vector<int> > goal(7, vector<int> ( 7,2));
    for(int i=0; i<7; i++){
        for(int j=0; j<7; j++){
            if(i==0 || i==1 || i==5 || i==6){
                    if(j==2 || j==3 || j==4){
                        goal[i][j]=0;
                    }
                }
                else{
                    goal[i][j]=0;
                }
        }
    }
    goal[3][3]=1;
}
bool goalTest(vector<vector<int> > state){
    return state==goal;
}

vector<Node*> getSuccessors(Node* nd){
    vector<Node*> ans;
    int dx2[] = {0,0,2,-2};
    int dy2[] = {-2,2,0,0};
    int dx1[] = {0,0,1,-1};
    int dy1[] = {-1,1,0,0};
    for(int i=0; i<7; i++){
        for(int j=0; j<7; j++){
            if(nd->state[i][j]==1){
                for(int k=0; k<4; k++){
                    int c2i = i+dy2[k];
                    int c2j = j+dx2[k];
                    int c1i = i+dy1[k];
                    int c1j = j+dx1[k];
                    if(c2i<0 || c2i>=7 || c2j<0 || c2j>=7) continue;
                    if(nd->state[c1i][c1j]==0) continue;
                    if(nd->state[c2i][c2j]==0){
                        vector<vector<int> > cpy = nd->state;
                        Node* chld = new Node(cpy,nd,nd->pathCost+1);
                        chld->state[c2i][c2j]=1;
                        chld->state[i][j]=0;
                        chld->state[c1i][c1j] = 0;
                        pair<int,int> p1(i,j);
                        pair<int,int> p2(c2i,c2j);
                        chld->action.first=p1;
                        chld->action.second=p2;
                        ans.push_back(chld);
                    }
                }
            }
        }
    }
    return ans;
}

struct hashFunction 
      {
         size_t operator()(const vector<vector<int> > &myVector) const 
         {
             std::hash<int> hasher;
             size_t answer = 0;
             for (vector<int> v : myVector) 
            {
                for(int j=0; j<v.size(); j++){
                    answer ^= hasher(v[j]) + 0x9e3779b9 + 
                                  (answer << 6) + (answer >> 2);
                }
           }
           return answer;
       }
   };

void displayBoard(vector<vector<int> > states){
    for(int i=0; i<7; i++){
        for(int j=0; j<7; j++){
            cout<<states[i][j]<<" ";
        }
        cout<<endl;
    }
}

Node* uCostSearch(){ // returns Goal node
    // cout<<"Entered uCostSearch"<<endl;
    Node* root = new Node(); // initial state and initial path cost are taken care of through constructor
    setGoal();
    priority_queue<Node*, vector<Node*>, compareCost> frontier; // ordered by path cost 
    unordered_set<vector<vector<int> >, hashFunction> explored; // keep states which are explored

    frontier.push(root);
    while(true){
        cout<<"frontier size: "<<frontier.size()<<endl;
        cout<<"explored size: "<<explored.size()<<endl;
        
        // cout<<"Entered while true"<<endl;
        if(frontier.empty()) return NULL; // failure
        Node* nd = frontier.top();

        // displayBoard(nd->state);
        cout<<"path cost: "<<(nd->pathCost)<<endl;
        cout<<endl;

        frontier.pop();
        if(explored.find(nd->state)!=explored.end()){
            continue;
        }

        if(goalTest(nd->state)){ 
            cout<<"Search ended"<<endl;
            cout<<"Toatal nodes explored: "<<(explored.size())<<endl;
            cout<<endl;
            return nd;
        }

        vector<Node*> children = getSuccessors(nd);
        // cout<<"children vector size: "<<children.size()<<endl;
        
        for(Node* child : children){
            // displayBoard(child->state);
            // cout<<endl;
           if(explored.find(child->state)==explored.end()){
            // cout<<"flag2"<<endl;
            frontier.push(child);
           }
        }
        explored.insert(nd->state);
        // vector<vector<vector<int> > > eqs = equivalents(nd->state);
        // for(vector<vector<int> > eq : eqs){
        //     explored.insert(eq);
        // }
    }
}

int main(){
    Node* goal;
    cout<<"Search started"<<endl;
    goal = uCostSearch();

    for(int i=0; i<7; i++){
        for(int j=0; j<7; j++){
            cout<<goal->state[i][j]<<" ";
        }
        cout<<endl;
    }
    return 0;
}