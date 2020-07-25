import pre_processing as pp

def main():
    months = ["2020\\01\\", "2020\\02\\", "2020\\03\\", "2020\\04\\", "2020\\05\\", "2020\\06\\"]
    for month in months:
        pp.df_compile(month)

if __name__ == '__main__':
    main()