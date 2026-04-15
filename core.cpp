#include <iostream>
#include <string>
#include <map>
#include <cstring>
#include <sstream>

using namespace std;

// Cấu trúc Node của Radix Trie
struct RadixNode {
    string edge_label;
    string data;
    bool is_end_of_word;
    map<char, RadixNode*> children;

    RadixNode(string label = "", string d = "", bool end = false) 
        : edge_label(label), data(d), is_end_of_word(end) {}
};

class RadixTrie {
private:
    RadixNode* root;

    // Hàm in cấu trúc cây (trực quan hóa)
    void printTree(RadixNode* node, int level, stringstream& ss) {
        if (!node) return;
        for (auto const& [key, child] : node->children) {
            for (int i = 0; i < level; ++i) ss << "  |";
            ss << "---[" << child->edge_label << "]";
            
            if (child->is_end_of_word) {
                string full_data = child->data;
                size_t pos = 0;
                while ((pos = full_data.find("||", pos)) != string::npos) {
                     full_data.replace(pos, 2, " ; ");
                     pos += 3;
                }
                ss << " => (" << full_data << ")";
            }
            ss << "\n";
            printTree(child, level + 1, ss);
        }
    }

    // Hàm đệ quy xử lý Xóa và Cắt tỉa nhánh rác (Pruning)
    bool removeHelper(RadixNode* node, string word, int i) {
        if (i == word.length()) {
            if (!node->is_end_of_word) return false;
            node->is_end_of_word = false;
            node->data = "";
            return true;
        }

        char c = word[i];
        if (node->children.find(c) == node->children.end()) return false;

        RadixNode* child = node->children[c];
        string label = child->edge_label;
        
        int j = 0;
        while (j < label.length() && i + j < word.length() && label[j] == word[i + j]) j++;
        
        if (j < label.length()) return false; // Lệch tiền tố

        bool isDeleted = removeHelper(child, word, i + j);

        if (isDeleted) {
            // Pruning 1: Node con rỗng -> Xóa hẳn
            if (child->children.empty() && !child->is_end_of_word) {
                delete child;
                node->children.erase(c);
            } 
            // Pruning 2: Node con chỉ có 1 nhánh -> Gộp Node
            else if (child->children.size() == 1 && !child->is_end_of_word) {
                auto it = child->children.begin();
                RadixNode* grandchild = it->second;
                
                child->edge_label += grandchild->edge_label;
                child->is_end_of_word = grandchild->is_end_of_word;
                child->data = grandchild->data;
                child->children = grandchild->children;
                
                delete grandchild;
            }
        }
        return isDeleted;
    }

public:
    RadixTrie() { root = new RadixNode(); }

    void insert(string word, string data) {
        RadixNode* curr = root;
        int i = 0;
        while (i < word.length()) {
            char c = word[i];
            if (curr->children.find(c) == curr->children.end()) {
                curr->children[c] = new RadixNode(word.substr(i), data, true);
                return;
            }

            RadixNode* child = curr->children[c];
            string label = child->edge_label;

            int j = 0;
            while (j < label.length() && i + j < word.length() && label[j] == word[i + j]) j++;

            // Split node (Chẻ nhánh)
            if (j < label.length()) {
                string common_prefix = label.substr(0, j);
                string remaining_label = label.substr(j);
                string remaining_word = word.substr(i + j);

                RadixNode* splitNode = new RadixNode(remaining_label, child->data, child->is_end_of_word);
                splitNode->children = child->children;

                child->edge_label = common_prefix;
                child->is_end_of_word = false;
                child->data = "";
                child->children.clear();
                child->children[remaining_label[0]] = splitNode;

                if (i + j < word.length()) {
                    child->children[remaining_word[0]] = new RadixNode(remaining_word, data, true);
                } else {
                    child->is_end_of_word = true;
                    child->data = data;
                }
                return;
            }

            if (j == label.length() && i + j < word.length()) {
                curr = child;
                i += j;
            } 
            // Cập nhật nghĩa cho từ đã tồn tại
            else if (j == label.length() && i + j == word.length()) {
                child->is_end_of_word = true;
                
                if (child->data.empty()) {
                    child->data = data;
                } else if (child->data.find(data) == string::npos) {
                    child->data += "||" + data; 
                }
                return;
            }
        }
    }

    string search(string word) {
        RadixNode* curr = root;
        int i = 0;
        while (i < word.length()) {
            char c = word[i];
            if (curr->children.find(c) == curr->children.end()) return "NOT_FOUND";
            
            RadixNode* child = curr->children[c];
            string label = child->edge_label;
            
            int j = 0;
            while (j < label.length() && i + j < word.length() && label[j] == word[i + j]) j++;
            if (j < label.length()) return "NOT_FOUND";
            
            curr = child;
            i += j;
        }
        return curr->is_end_of_word ? curr->data : "NOT_FOUND";
    }

    bool remove(string word) {
        return removeHelper(root, word, 0);
    }

    string visualize() {
        stringstream ss;
        ss << "[Root]\n";
        printTree(root, 0, ss);
        return ss.str();
    }
};

RadixTrie global_trie;
char buffer[10240]; 

extern "C" {
    void add_word(const char* word, const char* data) {
        global_trie.insert(string(word), string(data));
    }

    const char* find_word(const char* word) {
        string result = global_trie.search(string(word));
        strncpy(buffer, result.c_str(), sizeof(buffer));
        return buffer;
    }

    int delete_word(const char* word) {
        return global_trie.remove(string(word)) ? 1 : 0;
    }

    const char* get_trie_state() {
        string result = global_trie.visualize();
        strncpy(buffer, result.c_str(), sizeof(buffer));
        return buffer;
    }
}