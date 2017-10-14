#include<iostream>
#include<vector>
#include<queue>
#include<algorithm>
#include<ctime>
#include<climits>
#include<cstdio>

using namespace std;

#define toDigit(c)  (c-'0')

static int makeMoveCounter=0;
static int generatePossibleMovesCounter=0;
static int firstLeafDepth=0;
static int depthMax=0;
static int maxMoves = INT_MAX;
static float t = 0;

struct Move {
    int row;
    int col;
    int score;
};

struct Node {
    vector< vector<int> > board;
    int score;
};

bool compareByScore(Move a, Move b){            //ascending
    return a.score<b.score;
}

bool compareByScoreRev(Move a, Move b){         //descending
    return a.score>b.score;
}

bool isLeaf(Node node){
    int n = node.board.size();
    for(int i=0; i<n; i++){
        for(int j=0; j<n; j++){
            if(node.board[i][j] != -1)
                return false;
        }
    }

    return true;
}

Node applyGravity(Node node){
    int n = node.board.size();
    vector< vector<int> > board2(n, vector<int>(n, -1));
    int i, j, i2;

    for(j=0;j<n;j++){
        i2 = n-1;
        for(i=n-1; i>=0; i--){
            if(node.board[i][j] != -1){
                board2[i2][j] = node.board[i][j];
                i2--;
            }
        }
    }

    node.board = board2;

    return node;

}

Node makeMove(Node node, Move move, bool isMax){

    ++makeMoveCounter;

    Move temp;
    queue<Move> q;
    int n = node.board.size();
    int i, j, row, col, size = 1;
    vector<vector<bool> > visited(n, vector<bool>(n, false));

    q.push(move);
    visited[move.row][move.col] = !visited[move.row][move.col];
    while(!q.empty()){
        row = q.front().row;
        col = q.front().col;
        q.pop();

        // check neighbors
        if(row-1>=0){           //up
            if(!visited[row-1][col] && node.board[row-1][col] == node.board[move.row][move.col]) {        //check if something needs to be i or j
                size++;
                visited[row-1][col] = !visited[row-1][col];
                temp.row = row-1;
                temp.col = col;
                temp.score = 0;              // doesn't matter
                q.push(temp);
                node.board[row-1][col] = -1;
            }
        }

        if(row+1<n){           //down
            if(!visited[row+1][col] && node.board[row+1][col] == node.board[move.row][move.col]) {        //check if something needs to be i or j
                size++;
                visited[row+1][col] = !visited[row+1][col];
                temp.row = row+1;
                temp.col = col;
                temp.score = 0;              // doesn't matter
                q.push(temp);
                node.board[row+1][col] = -1;
            }
        }

        if(col-1>=0){           //left
            if(!visited[row][col-1] && node.board[row][col-1] == node.board[move.row][move.col]) {        //check if something needs to be i or j
                size++;
                visited[row][col-1] = !visited[row][col-1];
                temp.row = row;
                temp.col = col-1;
                temp.score = 0;              // doesn't matter
                q.push(temp);
                node.board[row][col-1] = -1;
            }
        }

        if(col+1<n) {           //right
            if (!visited[row][col + 1] && node.board[row][col + 1] == node.board[move.row][move.col]) {        //check if something needs to be i or j
                size++;
                visited[row][col + 1] = !visited[row][col + 1];
                temp.row = row;
                temp.col = col + 1;
                temp.score = 0;              // doesn't matter
                q.push(temp);
                node.board[row][col + 1] = -1;
            }
        }
    }
    node.board[move.row][move.col] = -1;
    node.score = isMax?(node.score + move.score):(node.score - move.score);

    node = applyGravity(node);

    return node;
}

vector<Move> generatePossibleMoves(vector<vector<int> > board, bool isMax){

    ++generatePossibleMovesCounter;

    vector<Move> movesList;
    Move move, temp;
    queue<Move> q;
    int n = board.size();
    int n2 = n*n;
    int i, j, row, col, size;
    vector<vector<bool> > visited(n, vector<bool>(n, false));

    for(i=0; i<n; i++){
        for(j=0; j<n; j++){
            if(!visited[i][j] && board[i][j]>=0){
                visited[i][j] = !visited[i][j];
                move.row = i;
                move.col = j;
                size = 1;

                q.push(move);
                while(!q.empty()){
                    row = q.front().row;
                    col = q.front().col;
                    q.pop();

                    // check neighbors
                    if(row-1>=0){           //up
                        if(!visited[row-1][col] && board[row-1][col] == board[row][col]) {        //check if something needs to be i or j
                            size++;
                            visited[row-1][col] = !visited[row-1][col];
                            temp.row = row-1;
                            temp.col = col;
                            temp.score = 0;              // doesn't matter
                            q.push(temp);
                        }
                    }

                    if(row+1<n){           //down
                        if(!visited[row+1][col] && board[row+1][col] == board[row][col]) {        //check if something needs to be i or j
                            size++;
                            visited[row+1][col] = !visited[row+1][col];
                            temp.row = row+1;
                            temp.col = col;
                            temp.score = 0;              // doesn't matter
                            q.push(temp);
                        }
                    }

                    if(col-1>=0){           //left
                        if(!visited[row][col-1] && board[row][col-1] == board[row][col]) {        //check if something needs to be i or j
                            size++;
                            visited[row][col-1] = !visited[row][col-1];
                            temp.row = row;
                            temp.col = col-1;
                            temp.score = 0;              // doesn't matter
                            q.push(temp);
                        }
                    }

                    if(col+1<n){           //right
                        if(!visited[row][col+1] && board[row][col+1] == board[row][col]) {        //check if something needs to be i or j
                            size++;
                            visited[row][col+1] = !visited[row][col+1];
                            temp.row = row;
                            temp.col = col+1;
                            temp.score = 0;              // doesn't matter
                            q.push(temp);
                        }
                    }
                }
                //visited children of move.
                move.score = size*size;
                movesList.push_back(move);
            }

        }
    }

    if(isMax) sort(movesList.begin(), movesList.end() , compareByScoreRev);
    else sort (movesList.begin(), movesList.end() , compareByScore);
    return movesList;       //return list of all possible moves = row, col, score
}

int minimax(Node node, int depth, bool isMax, int alpha, int beta){
    int best, movesListSize, value;
    int i, j, n=node.board.size();
    vector<Move> movesList;
    Node newState;

    if(isLeaf(node)){
        if(firstLeafDepth==0){
            firstLeafDepth = depth;
            int myMoves = (depth+10)/2;
            float t1 = 0.0001;
            float t2 = (0.9*t)/myMoves;     //time per move
            maxMoves = t2/t1;

        }
        return node.score;
    }


    if(makeMoveCounter >= (0.85*maxMoves)){
        return node.score;
    }


    if(isMax){
        best = INT_MIN;
        movesList = generatePossibleMoves(node.board, isMax);
        movesListSize = movesList.size();
        for(i=0; i<movesListSize; i++){
            newState = makeMove(node, movesList[i], isMax);
            value = minimax(newState, depth+1, !isMax, alpha, beta);
            best = max(best, value);
            alpha = max(alpha, best);
            if(beta<=alpha)     break;
        }
    }
    else{
        best = INT_MAX;
        movesList = generatePossibleMoves(node.board, isMax);
        movesListSize = movesList.size();
        for(i=0; i<movesListSize; i++){
            newState = makeMove(node, movesList[i], isMax);
            value = minimax(newState, depth+1, !isMax, alpha, beta);
            best = min(best, value);
            beta = min(beta, best);
            if (beta<=alpha)    break;
        }
    }

    return best;
}

Move findBestMove(Node root){

    Move move;      // best move
    Node newState;
    int possibleMovesSize;
    int bestVal = INT_MIN, i, movesListSize;

    vector<Move> movesList;
    movesList = generatePossibleMoves(root.board, true);
    movesListSize = movesList.size();

    for(i=0;i<movesListSize;i++){

        newState = makeMove(root, movesList[i], true);
        int moveVal = minimax(newState, 0, false, INT_MIN, INT_MAX);
        if (moveVal > bestVal){
            move.row = movesList[i].row;
            move.col = movesList[i].col;
            bestVal = moveVal;
        }
    }

//    cout<<"\nBestVal: "<<bestVal<<endl;

    return move;
}


int main(){

    clock_t tStart = clock();

    int i, j, n, p;
    char x;
    vector<int> row;
    vector< vector<int> > board;
    Move move;
    Node root;

    freopen("input.txt", "r", stdin);
    freopen("output.txt", "w", stdout);

    // ip
    cin>>n>>p;
    cin>>t;
    maxMoves = t*5000;

    for(i=0; i<n; i++){
        for(j=0; j<n; j++){
            cin>>x;
//            cout<<"x: "<<x;
            if(x=='*')  row.push_back(-1);
            else row.push_back(toDigit(x));
        }
//        cin>>x;
        board.push_back(row);
        row.clear();
    }

    root.board = board;
    root.score = 0;
    move = findBestMove(root);
    root = makeMove(root, move, true);

    //print op
    cout<<char('A'+move.col)<<(move.row+1)<<endl;  //Format B1 => B = 2nd col, row = 1
    for(i=0;i<n;i++){
        for(j=0;j<n;j++){
            if (root.board[i][j] == -1) cout<<"*";
            else cout<<root.board[i][j];
        }
        cout<<endl;
    }

//    printf("Time taken: %.8fs\n", (double)(clock() - tStart)/CLOCKS_PER_SEC);
//
//    cout<<endl<<"Generate Possible Moves Counter = "<<generatePossibleMovesCounter<<endl;
//    cout<<endl<<"Make Moves Counter = "<<makeMoveCounter<<endl;
//    cout<<endl<<"First depth = "<<firstLeafDepth<<endl;

    return 0;
}

