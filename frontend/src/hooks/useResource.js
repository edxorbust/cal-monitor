import { useCallback, useEffect, useState } from 'react';
import api from '../api/api';
import { errorMessage, listAll } from '../api/tracker';

export default function useResource(path, list = false) {
  const [data, setData] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);
  const [version, setVersion] = useState(0);
  const reload = useCallback(() => setVersion((value) => value + 1), []);
  useEffect(() => {
    let active = true;
    setLoading(true);
    setError('');
    const request = list ? listAll(path) : api.get(path).then((response) => response.data);
    request.then((result) => { if (active) setData(result); })
      .catch((err) => { if (active) setError(errorMessage(err)); })
      .finally(() => { if (active) setLoading(false); });
    return () => { active = false; };
  }, [path, list, version]);
  return { data, error, loading, reload };
}
