import numpy as np
import yaml

def save_numpy_to_yaml(numpy_array, filename="data.yaml"):
    """
    Salva um array NumPy em um arquivo YAML.

    Args:
        numpy_array (np.ndarray): O array NumPy a ser salvo.
        filename (str): O nome do arquivo YAML (com extensão .yaml).
    """
    try:
        # Converta o array NumPy para uma lista Python
        # Isso é necessário porque o PyYAML não pode serializar diretamente objetos NumPy.
        python_list = numpy_array.tolist()

        with open(filename, 'w') as file:
            yaml.dump(python_list, file)

        print(f"Array NumPy salvo com sucesso em '{filename}'")

    except Exception as e:
        print(f"Ocorreu um erro ao salvar o array NumPy: {e}")

def load_numpy_from_yaml(filename="data.yaml"):
    """
    Carrega um array NumPy de um arquivo YAML.

    Args:
        filename (str): O nome do arquivo YAML (com extensão .yaml).

    Returns:
        np.ndarray: O array NumPy carregado.
    """
    try:
        with open(filename, 'r') as file:
            python_list = yaml.safe_load(file)

        # Converta a lista Python de volta para um array NumPy
        numpy_array = np.array(python_list)
        print(f"Array NumPy carregado com sucesso de '{filename}'")
        return numpy_array

    except FileNotFoundError:
        print(f"Erro: O arquivo '{filename}' não foi encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro ao carregar o array NumPy: {e}")
        return None
def save_multiple_numpy_to_yaml(numpy_arrays_dict: dict, filename:str="data.yaml"):
    """
    Salva múltiplos arrays NumPy de um dicionário em um arquivo YAML.

    Args:
        numpy_arrays_dict (dict): Um dicionário onde as chaves são nomes (strings)
                                  e os valores são arrays NumPy.
        filename (str): O nome do arquivo YAML (com extensão .yaml).
    """
    try:
        data_to_save = {}
        for name, array in numpy_arrays_dict.items():
            if isinstance(array, np.ndarray):
                # Converte cada array NumPy para uma lista Python
                data_to_save[name] = array.tolist()
            else:
                print(f"Aviso: O valor para a chave '{name}' não é um array NumPy e será salvo como está.")
                data_to_save[name] = array

        with open(filename, 'w') as file:
            yaml.dump(data_to_save, file, default_flow_style=False, allow_unicode=True)

        print(f"Múltiplos arrays NumPy salvos com sucesso em '{filename}'")

    except Exception as e:
        print(f"Ocorreu um erro ao salvar os arrays NumPy: {e}")

def load_multiple_numpy_from_yaml(filename:str="data.yaml"):
    """
    Carrega múltiplos arrays NumPy de um arquivo YAML.

    Args:
        filename (str): O nome do arquivo YAML (com extensão .yaml).

    Returns:
        dict: Um dicionário onde as chaves são nomes (strings)
              e os valores são os arrays NumPy carregados.
    """
    try:
        with open(filename, 'r') as file:
            loaded_data = yaml.safe_load(file)

        loaded_numpy_arrays = {}
        if isinstance(loaded_data, dict):
            for name, data_list in loaded_data.items():
                # Converte cada lista de volta para um array NumPy
                loaded_numpy_arrays[name] = np.array(data_list)
            print(f"Múltiplos arrays NumPy carregados com sucesso de '{filename}'")
            return loaded_numpy_arrays
        else:
            print(f"Erro: O conteúdo do arquivo '{filename}' não é um dicionário. Não foi possível carregar como múltiplos arrays.")
            return {}

    except FileNotFoundError:
        print(f"Erro: O arquivo '{filename}' não foi encontrado.")
        return {}
    except Exception as e:
        print(f"Ocorreu um erro ao carregar os arrays NumPy: {e}")
        return {}

def concatenate_numpy_arrays_from_tuple(tuple_of_arrays, axis=0):
    """
    Converte uma tupla de arrays NumPy em um único array NumPy
    usando np.concatenate().

    Args:
        tuple_of_arrays (tuple): Uma tupla contendo arrays NumPy.
        axis (int, optional): O eixo ao longo do qual os arrays serão concatenados.
                              Padrão é 0 (linha).

    Returns:
        np.ndarray: Um único array NumPy resultante da concatenação.
    """
    if not all(isinstance(arr, np.ndarray) for arr in tuple_of_arrays):
        raise TypeError("Todos os elementos da tupla devem ser arrays NumPy.")
    if not tuple_of_arrays:
        return np.array([]) # Retorna um array vazio se a tupla for vazia

    try:
        result_array = np.concatenate(tuple_of_arrays, axis=axis)
        print(f"Arrays concatenados com sucesso ao longo do eixo {axis}.")
        return result_array
    except ValueError as e:
        print(f"Erro ao concatenar arrays: {e}")
        print("Verifique se os arrays têm dimensões compatíveis para a concatenação no eixo especificado.")
        return None

if __name__ == "__main__":
    # 1. Crie múltiplos arrays NumPy de exemplo
    array1 = np.array([[1, 2], [3, 4]])
    array2 = np.array([10, 20, 30])
    array3 = np.zeros((2, 3))
    array4 = np.ones((1, 5))

    # 2. Organize os arrays em um dicionário
    my_arrays_to_save = {
        "primeiro_array": array1,
        "segundo_array": array2,
        "zeros_array": array3,
        "ones_array": array4
    }

    print("Arrays NumPy originais:")
    for name, arr in my_arrays_to_save.items():
        print(f"--- {name} ---")
        print(arr)

    # 3. Salve o dicionário de arrays NumPy em um arquivo YAML
    save_multiple_numpy_to_yaml(my_arrays_to_save, "my_multiple_numpy_data.yaml")

    # 4. Carregue os arrays NumPy do arquivo YAML
    loaded_arrays = load_multiple_numpy_from_yaml("my_multiple_numpy_data.yaml")

    # 5. Verifique se os arrays carregados são iguais aos originais
    if loaded_arrays:
        print("\nArrays NumPy carregados:")
        for name, arr in loaded_arrays.items():
            print(f"--- {name} ---")
            print(arr)

        print("\nVerificando a igualdade dos arrays:")
        for name, original_arr in my_arrays_to_save.items():
            if name in loaded_arrays:
                loaded_arr = loaded_arrays[name]
                is_equal = np.array_equal(original_arr, loaded_arr)
                print(f"Array '{name}' é idêntico ao original: {is_equal}")
            else:
                print(f"Array '{name}' não foi encontrado no arquivo carregado.")
