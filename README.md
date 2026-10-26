# Page Replacement Algorithm Simulator

An Operating Systems lab project that simulates three page replacement algorithms: FIFO, LRU, and Optimal using Python in Jupyter Notebook.

## 📌 Project Overview

This project demonstrates how operating systems manage pages in memory when a page fault occurs and a replacement is required.

## 🚀 Features

- Implements FIFO (First-In, First-Out).
- Implements LRU (Least Recently Used).
- Implements Optimal Page Replacement.
- Accepts a page reference string and number of frames as user input.
- Displays step-by-step frame contents and page replacements.
- Calculates page faults, page hits, hit ratio, and fault ratio.
- Compares the performance of all three algorithms.
- Demonstrates Belady's anomaly.
- Includes manual tracing and experiments.

## 🛠️ Technologies Used

- Python
- Jupyter Notebook / Google Colab
- Pandas

## ▶️ How to Run

1. Download the `.ipynb` notebook from this repository.
2. Open [Google Colab](https://colab.research.google.com/).
3. Select **File → Upload notebook**.
4. Upload the notebook and run the cells in order.
5. Enter the page reference string and number of frames when prompted.

### Sample Input

```text
Page reference string: 1 2 3 1 4 2 5
Number of frames: 3
```

## 📊 Algorithms

| Algorithm | Replacement Rule |
|---|---|
| FIFO | Replaces the page that entered memory earliest. |
| LRU | Replaces the page least recently used in the past. |
| Optimal | Replaces the page whose next use is farthest in the future. |

## 🎯 Learning Outcomes

- Understanding page faults and page hits.
- Implementing page replacement algorithms.
- Comparing memory management strategies.
- Observing Belady's anomaly.

## 👨‍💻 Author

**Deep Dwivedi**

B.Tech CSE — Data Analytics

## 📚 Assignment

Operating Systems Lab — Virtual Memory and Page Replacement
