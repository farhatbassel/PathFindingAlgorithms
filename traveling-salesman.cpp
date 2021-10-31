#include <iostream>
#include <vector>
#include <limits>
#include <bits/stdc++.h>

using namespace std;
int n = 4;
int original_distances[10][10] = {
    {0, 10, 15, 20},
    {10, 0, 35, 25},
    {15, 35, 0, 30},
    {20, 25, 30, 0}};

int safe_copy[10][10] = {
    {0, 10, 15, 20},
    {10, 0, 35, 25},
    {15, 35, 0, 30},
    {20, 25, 30, 0}};

int start;
int new_graph[10][10];
int new_distances[10];
int VISITED_ALL = (1 << n) - 1;
bool exit_app = false;
char input;
vector<int> path;
int temporary_graph[10][10];

int add_node(int graph[10][10], int distances[10], int original[10][10]);
void print_graph(int graph[10][10]);
int remove_node(int removed_node, int graph[10][10]);
int get_shortest_path(int mask, int pos, int graph[10][10]);
int print_path();

int main()
{
    for (int i = 0; i < n + 1; i++)
        for (int j = 0; j < n + 1; j++)
        {
            new_graph[i][j] = original_distances[i][j];
        }

    cout << "The following program solves the Salesman Problem:" << endl;
    while (exit_app == false)
    {
        cout << "Enter 'h' to get an idea about how the program works." << endl;
        cout << "Enter 'p' to print the current graph." << endl;
        cout << "Enter 'a' to add a node to the already exsiting nodes." << endl;
        cout << "Enter 'r' to remove a node." << endl;
        cout << "Enter 'd' to restore the original graph." << endl;
        cout << "You can also enter 'q' at any time to exit the program." << endl;
        cin >> input;
        if (input == 'q')
        {
            exit_app = true;
        }
        if (input == 'h')
        {
            cout << "*********************************************" << endl;
            cout << "This program solves the shortest distances needed to get to all the points and back to the original point." << endl;
            cout << "The following matrix is an example that shows the distance between each city" << endl;
            print_graph(original_distances);
            cout << "The shortest distance in this graph is: ";
            cout << get_shortest_path(1, 0, original_distances) << endl;
            print_path();
            cout << "*********************************************" << endl;
        }
        if (input == 'a')
        {
            cout << "*********************************************" << endl;
            add_node(new_graph, new_distances, original_distances);
            cout << "New Graph: " << endl;
            n++;
            print_graph(new_graph);
            VISITED_ALL = (1 << n) - 1;
            cout << "The new shortest path has a distance of: ";
            cout << get_shortest_path(1, 0, new_graph) << endl;
            print_path();
            for (int i = 0; i < n + 1; i++)
                for (int j = 0; j < n + 1; j++)
                {
                    original_distances[i][j] = new_graph[i][j];
                }
            cout << "*********************************************" << endl;
        }
        if (input == 'r')
        {
            cout << "*********************************************" << endl;
            int remove;
            if (n > 2)
            {
                cout << "Which node would you like to remove?" << endl;
                print_graph(new_graph);
                cin >> remove;
                while ((cin.fail()) || (remove <= 0) || (remove > n))
                {
                    cin.clear();
                    cin.ignore(numeric_limits<streamsize>::max(), '\n');
                    cout << "The node you entered does not exist." << endl;
                    cout << "Please enter an existing node: ";
                    cin >> remove;
                }
                remove_node(remove - 1, new_graph);
                n--;
                print_graph(new_graph);
                VISITED_ALL = (1 << n) - 1;
                cout << "The new shortest path has a distance of: ";
                cout << get_shortest_path(1, 0, new_graph) << endl;
                print_path();
                cout << "*********************************************" << endl;
            }
            else
            {
                cout << "Minimum number of nodes reached" << endl;
                cout << "*********************************************" << endl;
            }
        }
        if (input == 'p')
        {
            cout << "*********************************************" << endl;
            cout << "The current graph looks as follows:" << endl;
            print_graph(new_graph);
            cout << "*********************************************" << endl;
        }
        if (input == 'd')
        {
            cout << "*********************************************" << endl;
            cout << "Default values have been restored." << endl;
	    n = 4;
 	    VISITED_ALL = (1 << n) - 1;
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++)
                {
                    new_graph[i][j] = safe_copy[i][j];
                }
            print_graph(new_graph);
            cout << "The shortest path has a distance of: ";
            cout << get_shortest_path(1, 0, new_graph) << endl;
            print_path();
            cout << "*********************************************" << endl;
        }
    }
    return 0;
}

int add_node(int graph[10][10], int distances[10], int original[10][10])
{
    for (int i = 0; i < n; i++)
    {
        cout << "Input the distance between the "
             << i + 1
             << " and " << n + 1 << " nodes: ";
        cin >> new_distances[i];
        while ((cin.fail()) || new_distances[i] <= 0)
        {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Please enter a positive integer: ";
            cin >> new_distances[i];
        }
    }
    for (int i = 0; i < n + 1; i++)
        for (int j = 0; j < n + 1; j++)
        {
            if (i == j)
            {
                graph[i][j] = 0;
            }
            else if (i == n)
            {
                graph[i][j] = distances[j];
            }
            else if (j == n)
            {
                graph[i][j] = distances[i];
            }
            else
            {
                graph[i][j] = original[i][j];
            }
        }
    return 0;
}

void print_graph(int graph[10][10])
{
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            cout << graph[i][j] << ' ';
        }
        cout << '\n';
    }
}

int print_path()
{
    cout << "The shortest path is: ";

    path.push_back(0);
    reverse(path.begin(), path.end());

    for (int i = 0; i < n; i++)
    {
        cout << path[i] + 1 << " ";
    }

    cout << path[0] + 1;
    cout << endl;

    path.clear();
    path.resize(n);

    return 0;
}
int remove_node(int removed_node, int graph[10][10])
{
    vector<vector<int>> vec(n);
    for (int i = 0; i < n; i++)
        vec[i].resize(n);

    for (int i = 0; i < vec.size(); i++)
    {
        for (int j = 0; j < vec[i].size(); j++)
        {
            vec[i][j] = graph[i][j];
            cout << vec[i][j] << " ";
        }
        cout << endl;
    }

    vec.erase(vec.begin() + removed_node);

    for (int i = 0; i < vec.size(); i++)
    {
        vec[i].erase(vec[i].begin() + removed_node);
    }

    cout << "The new node looks as follows: " << endl;
    for (int i = 0; i < vec.size(); i++)
    {
        for (int j = 0; j < vec[i].size(); j++)
        {
            new_graph[i][j] = vec[i][j];
        }
    }

    return 0;
}

int get_shortest_path(int mask, int pos, int graph[10][10])
{
    if (mask == VISITED_ALL)
    {
        return graph[pos][0];
    }

    int ans = INT_MAX;
    int val;

    for (int node = 0; node < n; node++)
    {

        if ((mask & (1 << node)) == 0)
        {
            int newAns = graph[pos][node] + get_shortest_path(mask | (1 << node), node, graph);

            if (newAns < ans)
            {
                ans = newAns;
                val = node;
                if (find(path.begin(), path.end(), val) == path.end())
                    path.push_back(val);
            }
        }
    }
    return ans;
}
